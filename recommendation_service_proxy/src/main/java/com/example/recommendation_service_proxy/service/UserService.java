package com.example.recommendation_service_proxy.service;

import com.example.recommendation_service_proxy.dto.JwtToken;
import com.example.recommendation_service_proxy.dto.UserDTO;
import com.example.recommendation_service_proxy.jwt.JwtProvider;
import com.example.recommendation_service_proxy.model.Role;
import com.example.recommendation_service_proxy.model.User;
import com.example.recommendation_service_proxy.repository.RoleRepository;
import com.example.recommendation_service_proxy.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final JwtProvider jwtProvider;

    @Autowired
    public UserService(UserRepository userRepository, RoleRepository roleRepository, JwtProvider jwtProvider) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.jwtProvider = jwtProvider;
    }

    public User getUserByLogin(String login) {
        return userRepository.findByLogin(login).orElseThrow(() -> new UsernameNotFoundException("User not found"));
    }

    public User getCurrentUser() {
        return getUserByLogin(SecurityContextHolder.getContext().getAuthentication().getName());
    }

    public JwtToken authentication(UserDTO dto) throws UsernameNotFoundException {
        User user = getUserByLogin(dto.getLogin());
        if (!new BCryptPasswordEncoder().matches(dto.getPassword(), user.getPassword()))
            throw new UsernameNotFoundException(String.format("Пользователь '%s' не найден", dto.getLogin()));
        String accessToken = jwtProvider.generateAccessToken(user);
        String refreshToken = jwtProvider.generateRefreshToken(user);
        return new JwtToken(accessToken, refreshToken);
    }

    public User registerUser(UserDTO dto) {
        User newUser = new User();
        newUser.setLogin(dto.getLogin());
        newUser.setPassword(new BCryptPasswordEncoder().encode(dto.getPassword()));
        newUser.setRoles(List.of(getDefaultRole()));
        userRepository.save(newUser);
        return getUserByLogin(dto.getLogin());
    }

    public Role getDefaultRole() {
        return roleRepository.findByName("user").orElseThrow(() -> new RuntimeException("Role not found"));
    }

}
