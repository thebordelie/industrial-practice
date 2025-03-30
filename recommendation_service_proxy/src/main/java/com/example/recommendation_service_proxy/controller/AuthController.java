package com.example.recommendation_service_proxy.controller;

import com.example.recommendation_service_proxy.dto.JwtToken;
import com.example.recommendation_service_proxy.dto.UserDTO;
import com.example.recommendation_service_proxy.model.User;
import com.example.recommendation_service_proxy.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping(value = "/auth")
public class AuthController {

    private final UserService userService;

    @Autowired
    public AuthController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("/login")
    public ResponseEntity<JwtToken> login(@RequestBody UserDTO userDTO) {
        return ResponseEntity.ok(userService.authentication(userDTO));
    }

    @PostMapping("/register")
    public ResponseEntity<User> register(@RequestBody UserDTO userDTO) {
        return ResponseEntity.ok(userService.registerUser(userDTO));
    }
}
