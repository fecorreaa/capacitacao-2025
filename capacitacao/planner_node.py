import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Point

class PlannerNode(Node):

    def __init__(self):
        super().__init__('planner_node')

        self.alvo_missao = Point(x=100.0, y=0.0, z=0.0)
        self.alvo_desvio = Point(x=100.0, y=20.0, z=50.0)
        
        self.pub_alvo = self.create_publisher(Point, '/alvo', 10)
        self.sub_alerta = self.create_subscription(Bool, '/alerta', self.decidir, 10)
        self.get_logger().info("Nó planner iniciado.")

    def decidir(self, msg):
        if msg.data == True:
            self.get_logger().info('Alerta de obstáculo recebido! A ordenar desvio...')
            self.pub_alvo.publish(self.alvo_desvio)
        else:
            self.get_logger().info('Caminho livre. A manter rota da missão...')
            self.pub_alvo.publish(self.alvo_missao)

def main():
    rclpy.init()
    planner_node = PlannerNode()
    rclpy.spin(planner_node)
    planner_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()