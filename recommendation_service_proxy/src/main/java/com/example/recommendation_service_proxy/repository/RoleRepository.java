package com.example.recommendation_service_proxy.repository;

import com.example.recommendation_service_proxy.model.Role;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface RoleRepository extends JpaRepository<
        Role, Integer> {

    Optional<Role> findByName(String name);
}
