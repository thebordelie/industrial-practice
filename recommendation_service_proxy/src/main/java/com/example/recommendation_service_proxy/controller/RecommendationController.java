package com.example.recommendation_service_proxy.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(value = "/visits")
public class RecommendationController {

    @GetMapping("/establishment")
    public ResponseEntity<String> getRecommendation() {
        return ResponseEntity.ok("Establishment");
    }
}
