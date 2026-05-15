package com.nithin.studentexamplanner.controller;

import com.nithin.studentexamplanner.dto.AskRequest;
import com.nithin.studentexamplanner.service.FastApiClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

// @RestController marks this class as a controller that returns JSON responses.
// @RequestMapping sets the base URL for all endpoints in this controller.
@RestController
@RequestMapping("/api/planner")
public class PlannerController {

    private final FastApiClient fastApiClient;

    // Constructor injection — never use @Autowired on fields.
    public PlannerController(FastApiClient fastApiClient) {
        this.fastApiClient = fastApiClient;
    }

    // POST /api/planner/ask — accepts a question, returns the RAG answer.
    @PostMapping("/ask")
    public String ask(@RequestBody AskRequest request) {
        return fastApiClient.getAnswer(request.getQuestion());
    }
}