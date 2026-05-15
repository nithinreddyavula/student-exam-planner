package com.nithin.studentexamplanner.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

// This DTO wraps the question into JSON format that FastAPI expects.
// Lombok generates the constructor and getters automatically.
@Data
@AllArgsConstructor
@NoArgsConstructor
public class AskRequest {
    private String question;
}
