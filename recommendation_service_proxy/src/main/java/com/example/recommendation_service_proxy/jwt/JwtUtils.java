package com.example.recommendation_service_proxy.jwt;

import com.example.recommendation_service_proxy.model.JwtAuthentication;
import com.example.recommendation_service_proxy.model.Role;
import io.jsonwebtoken.Claims;

import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Set;

public class JwtUtils {
    public static JwtAuthentication generate(Claims claims) {
        JwtAuthentication jwtInfoToken = new JwtAuthentication();
        jwtInfoToken.setRoles(getRoles(claims));
        jwtInfoToken.setFirstName(claims.get("firstName", String.class));
        jwtInfoToken.setUsername(claims.getSubject());
        return jwtInfoToken;
    }

    private static Set<Role> getRoles(Claims claims) {
        List roles = claims.get("roles", List.class);
        LinkedHashMap<Long, String> role = (LinkedHashMap<Long, String>) roles.get(0);
        Set<Role> roleSet = new HashSet<>();
        roleSet.add(new Role(1, role.get("name")));
        return roleSet;
    }
}
