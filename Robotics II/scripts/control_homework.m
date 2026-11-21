% 《机器人学 II》控制部分作业第 1–4 题
% 在 MATLAB 中打开本文件并运行。仅使用 MATLAB 自带的 ode45 和绘图函数。
% 各例均取零初值。机器人模型使用精确参数，不含饱和与时延。

solverOptions = odeset('RelTol', 1e-9, 'AbsTol', 1e-11);

%% 第 1 题：质量–弹簧–阻尼系统的 PID 比较
% x'' + 2*x' + 4*x = u，参考 r=1；微分作用于测量值。
pidCases = [4 0 0; 12 0 0; 12 8 0; 12 0 6; 12 8 6];
pidLabels = {'P: K_p=4', 'P: K_p=12', 'PI: K_i=8', ...
             'PD: K_d=6', 'PID: K_i=8, K_d=6'};
figure('Name', '1. PID parameter comparison');
hold on;
fprintf('\nQ1: Kp  Ki  Kd  peak(x)  x(12 s)\n');
for index = 1:size(pidCases, 1)
    gains = pidCases(index, :);
    [time, state] = ode45(@(~, z) pidDynamics(z, gains), ...
                         (0:0.01:12)', zeros(3, 1), solverOptions);
    plot(time, state(:, 1), 'LineWidth', 1.2);
    fprintf('%4g %4g %4g %8.4f %8.4f\n', ...
            gains(1), gains(2), gains(3), max(state(:, 1)), state(end, 1));
end
xlabel('t (s)'); ylabel('x (m)'); grid on;
legend(pidLabels, 'Location', 'southeast');

%% 第 2 题：单关节位置控制与速度反馈
Ra = 2;
J_eff = 0.02;
gamma = 0.11;
ka = 0.1;
ratio = 1/40;
kp = 6.4;
loadTorque = 0.5;  % 电机侧阻力矩，3 s 时接入
figure('Name', '2. Single-joint position feedback');
hold on;
fprintf('\nQ2: kv  peak(theta), before load  theta(8 s)\n');
for kv = [0, 2.1]
    [timeBefore, stateBefore] = ode45(@(~, z) jointDynamics(z, kv, 0, ...
        Ra, J_eff, gamma, ka, ratio, kp), (0:0.01:3)', zeros(2, 1), solverOptions);
    [timeAfter, stateAfter] = ode45(@(~, z) jointDynamics(z, kv, loadTorque, ...
        Ra, J_eff, gamma, ka, ratio, kp), (3:0.01:8)', stateBefore(end, :)', solverOptions);
    plot([timeBefore; timeAfter(2:end)], ...
         [stateBefore(:, 1); stateAfter(2:end, 1)], 'LineWidth', 1.2);
    fprintf('%4g %10.4f %10.4f\n', kv, max(stateBefore(:, 1)), stateAfter(end, 1));
end
xlabel('t (s)'); ylabel('\theta_L (rad)'); grid on;
legend('Position feedback', 'Position and velocity feedback', 'Location', 'southeast');

%% 第 3 题：两自由度耦合模型中的关节空间与笛卡尔空间阻抗
M = [2, 0.35; 0.35, 1.2];
H = [0.4, 0.05; 0.05, 0.3];  % h = H*q'
J = [1, 0.4; -0.25, 1.1];   % 局部模型 x = J*q
externalForce = [4; -2];
Mq = diag([1.5, 1]);
Bq = diag([6, 4]);
Kq = diag([6, 4]);
Mx = diag([2, 1]);
Bx = diag([8, 6]);
Kx = diag([8, 9]);
impedanceTime = (0:0.01:6)';
[timeQ, stateQ] = ode45(@(~, z) impedanceJointDynamics(z, M, H, J, ...
    externalForce, Mq, Bq, Kq), impedanceTime, zeros(4, 1), solverOptions);
[timeX, stateX] = ode45(@(~, z) impedanceTaskDynamics(z, M, H, J, ...
    externalForce, Mx, Bx, Kx), impedanceTime, zeros(4, 1), solverOptions);
taskPosition = stateX(:, 1:2) * J';
figure('Name', '3. Joint and Cartesian impedance');
subplot(2, 1, 1);
plot(timeQ, stateQ(:, 1:2), 'LineWidth', 1.2); grid on;
xlabel('t (s)'); ylabel('q (rad)'); legend('q_1', 'q_2', 'Location', 'east');
subplot(2, 1, 2);
plot(timeX, taskPosition, 'LineWidth', 1.2); grid on;
xlabel('t (s)'); ylabel('x (m)'); legend('x_1', 'x_2', 'Location', 'east');
fprintf('\nQ3: q(6 s) = [% .4f % .4f], x(6 s) = [% .4f % .4f]\n', ...
        stateQ(end, 1), stateQ(end, 2), taskPosition(end, 1), taskPosition(end, 2));

%% 第 4 题：约束系切向位控、法向力控
Sp = diag([1, 0]);
Sf = eye(2) - Sp;
xRef = [0.2; 0];
forceRef = [0; 5];
ke = 50;
[timeH, stateH] = ode45(@(~, z) hybridDynamics(z, M, H, J, Sp, Sf, ...
    xRef, forceRef, ke), (0:0.01:3)', zeros(4, 1), solverOptions);
positionH = stateH(:, 1:2) * J';
contactForce = ke * max(positionH(:, 2), 0);
figure('Name', '4. Hybrid position and force control');
subplot(2, 1, 1);
plot(timeH, positionH(:, 1), 'LineWidth', 1.2); grid on;
xlabel('t (s)'); ylabel('x_t (m)');
subplot(2, 1, 2);
plot(timeH, contactForce, 'LineWidth', 1.2); grid on;
xlabel('t (s)'); ylabel('f_e (N)');
rowAtOneSecond = find(abs(timeH - 1) < 1e-10, 1);
fprintf('\nQ4 at 1 s: x_t = %.4f m, f_e = %.4f N\n', ...
        positionH(rowAtOneSecond, 1), contactForce(rowAtOneSecond));

function dz = pidDynamics(z, gains)
    errorValue = 1 - z(1);
    input = gains(1)*errorValue + gains(2)*z(3) - gains(3)*z(2);
    dz = [z(2); input - 2*z(2) - 4*z(1); errorValue];
end

function dz = jointDynamics(z, kv, disturbance, Ra, J_eff, gamma, ka, ratio, kp)
    acceleration = (ka*kp*(1-z(1)) - (gamma+ka*kv)*z(2) ...
                    - ratio*Ra*disturbance) / (Ra*J_eff);
    dz = [z(2); acceleration];
end

function dz = impedanceJointDynamics(z, M, H, J, externalForce, Mq, Bq, Kq)
    q = z(1:2);
    velocity = z(3:4);
    externalTorque = J' * externalForce;
    desiredAcceleration = Mq \ (externalTorque - Bq*velocity - Kq*q);
    commandTorque = M*desiredAcceleration + H*velocity - externalTorque;
    physicalAcceleration = M \ (commandTorque + externalTorque - H*velocity);
    dz = [velocity; physicalAcceleration];
end

function dz = impedanceTaskDynamics(z, M, H, J, externalForce, Mx, Bx, Kx)
    velocity = z(3:4);
    x = J*z(1:2);
    xVelocity = J*velocity;
    taskAcceleration = Mx \ (externalForce - Bx*xVelocity - Kx*x);
    externalTorque = J' * externalForce;
    commandTorque = M*(J \ taskAcceleration) + H*velocity - externalTorque;
    physicalAcceleration = M \ (commandTorque + externalTorque - H*velocity);
    dz = [velocity; physicalAcceleration];
end

function dz = hybridDynamics(z, M, H, J, Sp, Sf, xRef, forceRef, ke)
    velocity = z(3:4);
    x = J*z(1:2);
    xVelocity = J*velocity;
    contact = [0; ke*max(x(2), 0)];
    positionAcceleration = 16*(xRef-x) - 8*xVelocity;
    % 虚拟质量 1 kg、比例力反馈增益 1、阻尼 20 N s/m。
    forceAcceleration = forceRef + (forceRef-contact) - 20*xVelocity - contact;
    taskAcceleration = Sp*positionAcceleration + Sf*forceAcceleration;
    contactTorque = J' * contact;
    commandTorque = M*(J \ taskAcceleration) + H*velocity + contactTorque;
    physicalAcceleration = M \ (commandTorque - contactTorque - H*velocity);
    dz = [velocity; physicalAcceleration];
end
