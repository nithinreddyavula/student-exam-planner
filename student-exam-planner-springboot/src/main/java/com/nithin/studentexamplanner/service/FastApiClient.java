package com.nithin.studentexamplanner.service;

import com.nithin.studentexamplanner.dto.AskRequest;
import com.nithin.studentexamplanner.dto.FastApiResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

// @Service marks this as a business logic component.
// RestTemplate is injected via constructor — always inject interfaces or beans, never instantiate manually.
@Service
public class FastApiClient {

    private final RestTemplate restTemplate;
    @Value("${fastapi.url}")
    private String FASTAPI_URL;

    public FastApiClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }
    @Cacheable(value = "ragAnswers", key = "#question")
    public String getAnswer(String question) {
        // Wrap the question into the request DTO
        AskRequest request = new AskRequest(question);

        // POST to FastAPI — Spring serializes AskRequest to JSON automatically
        // FastAPI response is deserialized into FastApiResponse automatically
        FastApiResponse response = restTemplate.postForObject(
                FASTAPI_URL,
                request,
                FastApiResponse.class
        );

        // Null check — if FastAPI returns nothing, return a safe fallback
        if (response == null || response.getAnswer() == null) {
            return "No answer received from RAG service.";
        }

        return response.getAnswer();
    }
}
