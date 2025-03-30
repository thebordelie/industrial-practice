package com.example.recommendation_service_proxy;

import com.example.recommendation_service_proxy.repository.RoleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class RecommendationServiceProxyApplication {

	public static void main(String[] args) {
		SpringApplication.run(RecommendationServiceProxyApplication.class, args);
	}

}
