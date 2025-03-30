package com.example.recommendation_service_proxy.service;

import com.example.recommendation_service_proxy.dto.RequestDTO;
import com.example.recommendation_service_proxy.model.Establishment;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class RecommendationService {

    public List<Establishment> getRecommendationsList(long userId) {
        List<Establishment> establishments = new ArrayList<>();
        return establishments;
    }


}
