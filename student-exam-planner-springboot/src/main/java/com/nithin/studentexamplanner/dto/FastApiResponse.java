package com.nithin.studentexamplanner.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.*;

// This DTO maps the JSON response from FastAPI back into a Java object.
// @JsonIgnoreProperties prevents errors if FastAPI adds extra fields.
@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class FastApiResponse {
    private String answer;
}
