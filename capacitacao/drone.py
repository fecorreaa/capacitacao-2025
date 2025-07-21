class SensorLiDAR:

    def __init__ (self):
        pass

    def medir_distancia (self, drone_altitude, altura_solo):
        
        distancia = drone_altitude - altura_solo

        if (distancia > 0):
            return distancia
        
        else:
            return 0
        
    
class Drone:
   
    def __init__(self, posicao_inicial=(0, 50), ambiente=None):
      
        # como o drone esta agora
        self.posicao_x = posicao_inicial[0]
        self.altitude_z = posicao_inicial[1]
        self.posicao_y = posicao_inicial[2]
        self.posicao_ang_z = posicao_inicial[3]

        # velocidades iniciais
        self.throttle = 0.0 
        self.roll = 0.0 
        self.pitch = 0.0
        self.yaw = 0.0

        self.altitude_alvo = 50
        self.y_alvo = 50

        self.lidar = SensorLiDAR()
        self.ambiente = ambiente

        self.moFL = 0.0
        self.moFR = 0.0
        self.moBL = 0.0
        self.moBR = 0.0

        
    def reportar_status(self):

        print(f"Posição: X = {self.posicao_x:.2f} |"
              f" Z = { self.altitude_z:.2f}, Alvo = {self.altitude_alvo:.2f} |"
              f"Y = {self.posicao_y:.2f}, Alvo = {self.y_alvo:.2f} | "
              f"Motores: [FL:{self.moFL:.2f}, FR:{self.moFR:.2f}, "
              f"BL:{self.moBL:.2f}, BR:{self.moBR:.2f}]")

    def executar(self):

        altura_solo = self.ambiente.obter_altura(self.posicao_x)
        altitude_atual = self.lidar.medir_distancia(self.altitude_z, altura_solo)

        erro_z = self.altitude_alvo - altitude_atual
        erro_y =self.y_alvo - self.posicao_y

        cmmd_thrust = erro_z * 0.5
        cmmd_pitch = 0.1
        cmmd_roll = erro_y * 0.5
        cmmd_yaw = 0

        self._motor_mixing(cmmd_thrust, cmmd_pitch, cmmd_roll, cmmd_yaw)

    def _motor_mixing(self, thrust, pitch, roll, yaw):

        thrust_b = 50 # v necessaria p anular a gravidade
        thrust_f = thrust_b + thrust

        self.moFL =thrust_f - pitch + roll - yaw
        self.moFR = thrust_f - pitch - roll + yaw
        self.moBL = thrust_f + pitch + roll + yaw
        self.moBR = thrust_f + pitch - roll - yaw

        #verificar se a v não é negativa

        if self.moFL < 0:
            self.moFL = 0

        if self.moFR < 0:
            self.moFR = 0
        
        if self.moBL < 0:
            self.moBL = 0

        if self.moBR < 0:
            self.moBR = 0
    
    def fisica(self):

        thrust_t = (self.moFL + self.moFR + self.moBL + self.moBR) / 4
        gravidade = 50

        #logica throttle
        aceleracao_t = (thrust_t - gravidade) * 0.1 
        self.throttle = self.throttle + aceleracao_t 
        self.altitude_z = self.altitude_z + self.throttle 
        self.throttle = self.throttle * 0.9 

        # logica roll
        aceleracao_r = ((self.moFL + self.moBL) - (self.moFR + self.moBR)) * 0.1
        self.roll += aceleracao_r
        self.posicao_y += self.roll 
        self.roll *= 0.95 

        #pitch
        aceleracao_p = ((self.moBL +  self.moBR) - (self.moFR + self.moFL))* 0.05
        self.pitch += aceleracao_p 
        self.posicao_x += self.pitch
        self.pitch *= 0.95

        #yaw
        aceleracao_y = ((self.moFR + self.moBL) - (self.moFL + self.moBR)) * 0.01
        self.yaw += aceleracao_y
        self.posicao_ang_z += self.yaw 

        altura_solo_atual = self.ambiente.obter_altura(self.posicao_x)
        if self.altitude_z < altura_solo_atual:
            self.altitude_z = altura_solo_atual
            self.throttle = 0