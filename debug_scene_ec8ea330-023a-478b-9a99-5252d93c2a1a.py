from manim import *
import math
import numpy as np

class CustomAnimation(Scene):
    def construct(self):
        # Define screen regions for better organization
        title_region = UP * 3.5
        main_region = ORIGIN
        explanation_region = DOWN * 3
        
        # Define safe boundaries for text placement
        boundary_threshold = 6  # Max distance from origin to stay in bounds
        
        def ensure_within_boundaries(position, threshold=boundary_threshold):
            '''Ensure a position is within the safe boundaries of the screen.'''
            if isinstance(position, np.ndarray):
                magnitude = np.linalg.norm(position)
                if magnitude > threshold:
                    return position * (threshold / magnitude)
            return position
        
        # INTRODUCTION [00:00]
        intro_text = Text("Welcome to our educational animation on load balancers.", font_size=24).move_to(ensure_within_boundaries(explanation_region))
        self.play(Write(intro_text), run_time=2)
        self.wait(1)
        
        # WHAT ARE LOAD BALANCERS? [00:30]
        self.play(FadeOut(intro_text))
        lb_text = Text("A load balancer acts as a single entry point for clients accessing a service or application.", font_size=24).move_to(ensure_within_boundaries(explanation_region))
        self.play(Write(lb_text), run_time=2)
        
        # Visual representation of load balancer
        clients = VGroup(*[Text("Client", font_size=18).move_to(ensure_within_boundaries((LEFT * 4 + UP * i)) for i in np.arange(-2, 3, 1)])
        lb = Text("Load Balancer", font_size=18).move_to(ensure_within_boundaries((ORIGIN))
        servers = VGroup(*[Text("Server", font_size=18).move_to(ensure_within_boundaries((RIGHT * 4 + UP * i)) for i in np.arange(-2, 3, 1)])
        
        self.play(Create(VGroup(clients, lb, servers)))
        self.wait(1)
        
        # Show traffic flow
        arrows = VGroup(*[Arrow(client.get_right(), lb.get_left(), color=BLUE) for client in clients] + 
        arrows.move_to(ensure_within_boundaries(ORIGIN))
                         [Arrow(lb.get_right(), server.get_left(), color=GREEN) for server in servers])
                         [Arrow(lb.get_right(), server.get_left(), color.move_to(ensure_within_boundaries(ORIGIN))
        self.play(Create(arrows), run_time=2)
        self.wait(1)
        
        # Clean up
        self.play(FadeOut(VGroup(clients, lb, servers, arrows, lb_text)))
        
        # VISUALIZING LOAD BALANCERS IN ACTION [01:15]
        lb_action_text = Text("The load balancer directs incoming requests across multiple backend servers.", font_size=24).move_to(ensure_within_boundaries(explanation_region))
        self.play(Write(lb_action_text), run_time=2)
        
        # Simple visualization of load balancer distributing requests
        request_arrows = VGroup(*[Arrow(LEFT * 3 + UP * (2 - i), RIGHT * 3 + UP * (2 - i), color=BLUE) for i in range(5)])
        lb_symbol = Text("LB", font_size=24).move_to(ensure_within_boundaries((ORIGIN))
        self.play(Create(lb_symbol), Create(request_arrows))
        self.wait(2)
        
        # Clean up
        self.play(FadeOut(VGroup(lb_symbol, request_arrows, lb_action_text)))
        
        # HOW LOAD BALANCERS WORK [02:00]
        lb_work_text = Text("Load balancers distribute workload across multiple servers using various algorithms.", font_size=24).move_to(ensure_within_boundaries(explanation_region))
        self.play(Write(lb_work_text), run_time=2)
        
        # Show different algorithms
        algo_text = VGroup(
            Text("Round Robin", font_size=18).move_to(ensure_within_boundaries((UP * 2)),
            Text("Least Connections", font_size=18).move_to(ensure_within_boundaries((ORIGIN)),
            Text("IP Hash", font_size=18).move_to(ensure_within_boundaries((DOWN * 2))
        )
        self.play(Create(algo_text), run_time=2)
        self.wait(2)
        
        # Clean up
        self.play(FadeOut(VGroup(algo_text, lb_work_text)))
        
        # SERVER HEALTH MONITORING [03:30]
        health_text = Text("Load balancers monitor server health and remove unresponsive servers from rotation.", font_size=24).move_to(ensure_within_boundaries(explanation_region))
        self.play(Write(health_text), run_time=2)
        
        # Simple visualization of health monitoring
        server_status = VGroup(
            Text("Server 1: Healthy", font_size=18, color=GREEN).move_to(ensure_within_boundaries((UP)),
            Text("Server 2: Unhealthy", font_size=18, color=RED).move_to(ensure_within_boundaries((DOWN))
        )
        self.play(Create(server_status))
        self.wait(2)
        
        # Clean up
        self.play(FadeOut(VGroup(server_status, health_text)))
        
        # ROLE IN REDUNDANCY AND HIGH AVAILABILITY [04:15]
        redundancy_text = Text("Load balancers contribute to redundancy and high availability by directing traffic to healthy servers.", font_size=24).move_to(ensure_within_boundaries(explanation_region))
        self.play(Write(redundancy_text), run_time=2)
        
        # Visualization of redundancy
        active_server = Text("Active Server", font_size=18, color=GREEN).move_to(ensure_within_boundaries((LEFT * 3))
        standby_server = Text("Standby Server", font_size=18, color=YELLOW).move_to(ensure_within_boundaries((RIGHT * 3))
        self.play(Create(VGroup(active_server, standby_server)))
        self.wait(2)
        
        # Simulate failover
        failed_server = Text("Failed Server", font_size=18, color=RED).move_to(ensure_within_boundaries((LEFT * 3))
        self.play(Transform(active_server, failed_server))
        self.wait(1)
        traffic_arrow = Arrow(active_server.get_right(), standby_server.get_left(), color=BLUE)
        traffic_arrow.move_to(ensure_within_boundaries(ORIGIN))
        self.play(Create(traffic_arrow))
        self.wait(1)
        
        # Clean up
        self.play(FadeOut(VGroup(active_server, standby_server, traffic_arrow, redundancy_text)))
        
        # REAL-WORLD EXAMPLES [05:00]
        example_text = Text("For example, an e-commerce website uses load balancers to distribute traffic during sales events.", font_size=24).move_to(ensure_within_boundaries(explanation_region))
        self.play(Write(example_text), run_time=2)
        
        # Simple visualization of e-commerce example
        ecommerce_lb = Text("E-commerce Load Balancer", font_size=18).move_to(ensure_within_boundaries((ORIGIN))
        user_requests = VGroup(*[Text("User Request", font_size=12).move_to(ensure_within_boundaries((LEFT * 3 + UP * (1.5 - i))) for i in range(3)])
        servers = VGroup(*[Text("Server", font_size=18).move_to(ensure_within_boundaries((RIGHT * 3 + UP * (1.5 - i))) for i in range(3)])
        self.play(Create(VGroup(ecommerce_lb, user_requests, servers)))
        request_arrows = VGroup(*[Arrow(user_request.get_right(), server.get_left(), color=BLUE) for user_request, server in zip(user_requests, servers)])
        request_arrows.move_to(ensure_within_boundaries(ORIGIN))
        self.play(Create(request_arrows))
        self.wait(2)
        
        # Clean up
        self.play(FadeOut(VGroup(ecommerce_lb, user_requests, servers, request_arrows, example_text)))
        
        # ADDITIONAL FEATURES AND BENEFITS [05:45]
        additional_features_text = Text("Load balancers can also handle SSL termination and layer 7 routing.", font_size=24).move_to(ensure_within_boundaries(explanation_region))
        self.play(Write(additional_features_text), run_time=2)
        
        # Simple visualization of additional features
        ssl_text = Text("SSL Termination", font_size=18).move_to(ensure_within_boundaries((UP))
        layer7_text = Text("Layer 7 Routing", font_size=18).move_to(ensure_within_boundaries((DOWN))
        self.play(Create(VGroup(ssl_text, layer7_text)))
        self.wait(2)
        
        # Clean up
        self.play(FadeOut(VGroup(ssl_text, layer7_text, additional_features_text)))
        
        # CONCLUSION [06:30]
        conclusion_text = Text("In conclusion, load balancers are crucial for scaling applications and maintaining high availability.", font_size=24).move_to(ensure_within_boundaries(explanation_region))
        self.play(Write(conclusion_text), run_time=2)
        self.wait(2)
        
        # Final clean up
        self.play(FadeOut(conclusion_text))
        self.wait(1)