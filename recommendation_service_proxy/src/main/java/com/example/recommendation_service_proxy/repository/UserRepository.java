package com.example.recommendation_service_proxy.repository;

import com.example.recommendation_service_proxy.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByLogin(String username);
    boolean existsByLogin(String login);
}
