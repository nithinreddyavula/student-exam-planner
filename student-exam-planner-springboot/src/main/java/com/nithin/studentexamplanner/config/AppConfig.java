package com.nithin.studentexamplanner.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

// @Configuration tells Spring this class provides beans.
// RestTemplate bean is registered here so it can be injected anywhere.
@Configuration
public class AppConfig {

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
