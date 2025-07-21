import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Point
from capacitacao.ambiente import Ambiente

class SensorNode(Node):

    def __init__(self, ambiente):
        super().__init__('sensor_node')

        self.ambiente = ambiente
        self.posicao = Point()

        self.alerta_pub = self.create_publisher(Bool, 'alerta', 10)
        self.posicao_sub = self.create_subscription(Point, 'posicao', self.callback, 10)
        self.timer = self.create_timer(0.1, self.verificar)
        self.get_logger().info("Nó sensor iniciado.")

    def callback(self, msg):
        self.posicao = msg

    def verificar(self):
        x_futuro = self.posicao.x + 5
        altura_frente = self.ambiente.obter_altura(x_futuro)
        
        alerta_msg = Bool()

        if altura_frente > 0 and self.posicao.z <= (altura_frente + 5):
            alerta_msg.data = True

        else:
            alerta_msg.data = False
        self.alerta_pub.publish(alerta_msg)


def main():
    rclpy.init()

    ambiente = Ambiente(tamanho = 100)
    sensor_node = SensorNode(ambiente)

    rclpy.spin(sensor_node)
    sensor_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()