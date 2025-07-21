import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from capacitacao.drone import Drone
from capacitacao.ambiente import Ambiente

class PilotNode(Node):

    def __init__(self, drone, ambiente):
        super().__init__('pilot_node')

        self.drone = drone
        self.ambiente = ambiente

        self.posicao_pub = self.create_publisher(Point, 'posicao', 10)
        self.alvo_sub = self.create_subscription(Point, 'alvo', self.callback, 10)
        self.timer = self.create_timer(0.1, self.passo)
        self.get_logger().info("Nó piloto iniciado")

    def callback(self, msg):

        self.drone.x_alvo = msg.x
        self.drone.y_alvo = msg.y
        self.drone.altitude_alvo = msg.z

    def passo(self):

        self.drone.executar()
        self.drone.fisica()

        posicao_msg = Point()
        posicao_msg.x = self.drone.posicao_x
        posicao_msg.y = self.drone.posicao_y
        posicao_msg.z = self.drone.altitude_z

        self.posicao_pub.publish(posicao_msg)


def main():
        rclpy.init()

        ambiente = Ambiente(tamanho = 100)
        drone = Drone(posicao_inicial = (0, 0, 0, 0), ambiente = ambiente)
        pilot_node = PilotNode(drone, ambiente)

        rclpy.spin(pilot_node)
        pilot_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()