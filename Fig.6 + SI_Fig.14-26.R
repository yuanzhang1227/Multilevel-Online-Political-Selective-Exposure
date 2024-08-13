library(ggplot2)
library(tidyverse)  
library(betareg)    
library(scales)    
library(ggrepel)   
library(VGAM)      
library(broom)      
library(kableExtra) 


## Regression results function
wrap_labels <- function(labels, width) {
  sapply(labels, function(x) paste(strwrap(x, width = width), collapse = "\n"))
}

theme_design <- theme(
  panel.grid.major = element_line(color = "gray", linetype = "dashed", size = 0.5),
  panel.grid.minor = element_blank(),
  panel.background = element_blank(),
  axis.ticks = element_blank(),
  axis.text.x = element_text(size = 32),
  axis.text.y = element_text(size = 45),
  axis.title.x = element_text(size = 48),
  plot.title = element_text(hjust = 0.5, size = 45, face = "bold"),
  plot.margin = margin(t = 1, r = 1, b = 1, l = 1, unit = "cm"),
  aspect.ratio = 1.7, 
  strip.background = element_rect(fill = "grey80", color = "black"),
  strip.text = element_text(size = 55, face = "bold")
)

create_plot <- function(data, labels, title, x_label = "Coefficient", decimals = 3, label_width = 10, x_limits = c(-0.5, 0.5), x_breaks = seq(-0.5, 0.5, 0.2)) {
  data$title <- title 
  wrapped_labels <- wrap_labels(labels, label_width)  
  names(wrapped_labels) <- names(labels)
  
  ggplot(data, aes(x = Coefficient, y = Variable)) +
    geom_segment(aes(x = Lower_CI, xend = Upper_CI, y = Variable, yend = Variable), color = "black", size = 2.5) +
    geom_pointrange(aes(xmin = Lower_CI, xmax = Upper_CI), color = "black", size = 2.5) +
    geom_vline(xintercept = 0, color = "red", size = 2) +
    geom_text(aes(label = round(Coefficient, decimals), x = Coefficient), vjust = -1, size = 12, color = "blue") +
    scale_y_discrete(labels = wrapped_labels) +
    scale_x_continuous(limits = x_limits, breaks = x_breaks) +  
    labs(x = x_label, y = "") +
    theme_bw() + nature_theme +
    facet_wrap(~title)
}


## Regression Analysis - Level 1
#### Community Overlap
model <- vglm(Overlap ~ Satisfactory.with.Democracy + Incivility.Perception_Impoliteness_Twitter  + Read.Watch_Twitter + Age + Ideological.Position, data = my_data, family = posnegbinomial())

#### Check distributions 
fitted_values <- fitted(model)
my_data$fitted_values <- fitted_values
mean_fitted <- mean(fitted_values)

# Calculate the parameters for the negative binomial distribution
size <- 1 / (mean_fitted - 1)
prob <- size / (size + mean_fitted)

# Generate negative binomial probabilities for the observed range
max_overlap <- max(my_data$Overlap)
nbinom_probs <- data.frame(
  Overlap = 1:max_overlap,
  Probability = dnbinom(1:max_overlap, size = size, mu = mean_fitted)
)

# Normalize negative binomial probabilities to sum to 1
nbinom_probs$Frequency <- nbinom_probs$Probability / sum(nbinom_probs$Probability)

# Normalize the observed Overlap values
total_overlap <- sum(my_data$Overlap)

overlap_distribution_1 <- ggplot(my_data, aes(x = Overlap)) +
  geom_histogram(aes(y = ..density..), binwidth = 1, fill = "skyblue", color = "black", alpha = 1) +
  geom_line(data = nbinom_probs, aes(x = Overlap, y = Frequency), color = "red", size = 2) +
  labs(title = "Community Overlap (Level 1)", x = "Values", y = "Normalized Frequency") +
  scale_x_continuous(breaks = pretty_breaks(), limits = c(0, max_overlap)) +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        panel.grid.major = element_line(color = "grey80"),
        panel.grid.minor = element_line(color = "grey80"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))


# Display the plot
print(overlap_distribution_1)
ggsave("./distribution1_level1.png", overlap_distribution_1, width = 8, height = 6, units = "in", dpi = 600)


coefficients <- coef(model)
conf_intervals <- confint.default(model)
rownames(conf_intervals)
plot_data_overlap <- data.frame(
  Variable = rownames(conf_intervals),
  Coefficient = coefficients[rownames(conf_intervals)],
  Lower_CI = conf_intervals[, 1],
  Upper_CI = conf_intervals[, 2]
)
plot_data_overlap <- plot_data_overlap[!rownames(plot_data_overlap) %in% c("(phi)", "(Intercept):1", "(Intercept):2"), ]
plot_data_overlap$Variable <- factor(plot_data_overlap$Variable, levels = rev(c("Ideological.Position", "Incivility.Perception_Impoliteness_Twitter", "Read.Watch_Twitter", "Age", "Satisfactory.with.Democracy")))

custom_labels_overlap<- c(
  "Satisfactory.with.Democracy" = "Democracy satisfaction",
  "Incivility.Perception_Impoliteness_Twitter" = "Incivility perception",
  "Read.Watch_Twitter" = "Twitter consumption",
  "Age" = "Age",
  "Ideological.Position" = "Ideological position"
)


#### Identity Diversity with nans
N <- nrow(my_data)
s <- 0.5
my_data$adjusted_proportion <- (my_data$Label_diversity_with_nans * (N - 1) + s) / N
model <- betareg(adjusted_proportion ~ Media.Trust_7, data = my_data)
summary(model)

coefficients <- coef(model)
conf_intervals <- confint.default(model)

plot_data_identity_diversity_with_nans <- data.frame(
  Variable = rownames(conf_intervals),
  Coefficient = coefficients[rownames(conf_intervals)],
  Lower_CI = conf_intervals[, 1],
  Upper_CI = conf_intervals[, 2]
)
plot_data_identity_diversity_with_nans <- plot_data_identity_diversity_with_nans[!rownames(plot_data_identity_diversity_with_nans) %in% c("(phi)", "(Intercept)"), ]
custom_labels_identity_diversity_with_nans <- c(
  "Media.Trust_7" = "Military trust"
)

#### Check distributions
fitted_mean <- fitted(model)

# Extract the precision parameter (phi)
precision <- model$coefficients$precision

# Calculate the shape parameters
mean_fitted_mean <- mean(fitted_mean, na.rm = TRUE)
shape1 <- mean_fitted_mean * precision
shape2 <- (1 - mean_fitted_mean) * precision

# Ensure that the adjusted_proportion has no NaNs or NAs
my_data_clean <- my_data[!is.na(my_data$adjusted_proportion) & !is.infinite(my_data$adjusted_proportion), ]

normalize_beta <- function(x) {
  dbeta(x, shape1, shape2) / 187 
}

label1_distribution_1 <- ggplot(my_data_clean, aes(x = adjusted_proportion)) +
  geom_histogram(aes(y = ..count../sum(..count..)), binwidth = 0.01, fill = "skyblue", color = "black", alpha = 1) +
  stat_function(
    fun = normalize_beta,
    color = "red",
    size = 2
  ) +
  labs(title = "Identity Diversity with Nans (Level 1)",
       x = "Values",
       y = "Normalized Frequency") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        panel.grid.major = element_line(color = "grey80"),
        panel.grid.minor = element_line(color = "grey80"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(label1_distribution_1)
ggsave("./distribution2_level1.png", label1_distribution_1, width = 8, height = 6, units = "in", dpi = 600)



#### Check residuals (with outliers)
fitted_values <- fitted(model)
residuals_values <- residuals(model)
residuals_data <- data.frame(Fitted = fitted_values, Residuals = residuals_values)
residuals_plot_2 <- ggplot(residuals_data, aes(x = Fitted, y = Residuals)) +
  geom_point() +
  geom_smooth(method = "loess", color = "red") +
  labs(title = "Identity Diversity (with Nans)",
       x = "Fitted Values",
       y = "Residuals") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(residuals_plot_2)

#### Check residuals (without outliers)
indexes_to_remove <- c()  
filtered_data <- my_data
N <- nrow(filtered_data)
s <- 0.5
filtered_data$adjusted_proportion <- (filtered_data$identity_diversity_with_nans * (N - 1) + s) / N
model <- betareg(adjusted_proportion ~ Media.Trust_7, data = filtered_data)

fitted_values <- fitted(model)
residuals_values <- residuals(model)
residuals_data <- data.frame(Fitted = fitted_values, Residuals = residuals_values, Index = 1:nrow(filtered_data))

# Create the residuals plot with annotations using ggrepel
residuals_plot_2_ro <- ggplot(residuals_data, aes(x = Fitted, y = Residuals)) +
  geom_point() +
  geom_smooth(method = "loess", color = "red") +
  labs(title = "Identity Diversity with Nans (Level 1)",
       x = "Fitted Values",
       y = "Residuals") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(residuals_plot_2_ro)

coefficients <- coef(model)
conf_intervals <- confint.default(model)

plot_data_identity_diversity_with_nans_ro <- data.frame(
  Variable = rownames(conf_intervals),
  Coefficient = coefficients[rownames(conf_intervals)],
  Lower_CI = conf_intervals[, 1],
  Upper_CI = conf_intervals[, 2]
)
plot_data_identity_diversity_with_nans_ro <- plot_data_identity_diversity_with_nans_ro[!rownames(plot_data_identity_diversity_with_nans_ro) %in% c("(phi)", "(Intercept)"), ]
custom_labels_identity_diversity_with_nans <- c(
  "Media.Trust_7" = "Military trust"
)


#### Identity Diversity without nans
N <- nrow(my_data)
s <- 0.5
my_data$adjusted_proportion <- (my_data$Label_diversity_without_nans * (N - 1) + s) / N
model <- betareg(adjusted_proportion ~ Media.Trust_7, data = my_data)
summary(model)

coefficients <- coef(model)
conf_intervals <- confint.default(model)

plot_data_identity_diversity_without_nans <- data.frame(
  Variable = rownames(conf_intervals),
  Coefficient = coefficients[rownames(conf_intervals)],
  Lower_CI = conf_intervals[, 1],
  Upper_CI = conf_intervals[, 2]
)
plot_data_identity_diversity_without_nans <- plot_data_identity_diversity_without_nans[!rownames(plot_data_identity_diversity_without_nans) %in% c("(phi)", "(Intercept)"), ]
custom_labels_identity_diversity_without_nans <- c(
  "Media.Trust_7" = "Military trust"
)

#### Check distributions 
fitted_mean <- fitted(model)

# Extract the precision parameter (phi)
precision <- model$coefficients$precision

# Calculate the shape parameters
mean_fitted_mean <- mean(fitted_mean, na.rm = TRUE)
shape1 <- mean_fitted_mean * precision
shape2 <- (1 - mean_fitted_mean) * precision

# Ensure that the adjusted_proportion has no NaNs or NAs
my_data_clean <- my_data[!is.na(my_data$adjusted_proportion) & !is.infinite(my_data$adjusted_proportion), ]

normalize_beta <- function(x) {
  dbeta(x, shape1, shape2) / 187 
}

label2_distribution_1 <- ggplot(my_data_clean, aes(x = adjusted_proportion)) +
  geom_histogram(aes(y = ..count../sum(..count..)), binwidth = 0.01, fill = "skyblue", color = "black", alpha = 1) +
  stat_function(
    fun = normalize_beta,
    color = "red",
    size = 2
  ) +
  labs(title = "Identity Diversity without Nans (Level 1)",
       x = "Values",
       y = "Normalized Frequency") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        panel.grid.major = element_line(color = "grey80"),
        panel.grid.minor = element_line(color = "grey80"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(label2_distribution_1)
ggsave("./distribution3_level1.png", label2_distribution_1, width = 8, height = 6, units = "in", dpi = 600)


#### Check residuals
fitted_values <- fitted(model)
residuals_values <- residuals(model)
residuals_data <- data.frame(Fitted = fitted_values, Residuals = residuals_values)
residuals_plot_3 <- ggplot(residuals_data, aes(x = Fitted, y = Residuals)) +
  geom_point() +
  geom_smooth(method = "loess", color = "red") +
  labs(title = "Identity Diversity (without nans)",
       x = "Fitted Values",
       y = "Residuals") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(residuals_plot_3)

#### Check residuals (without outliers)
indexes_to_remove <- c()  
filtered_data <- my_data
N <- nrow(filtered_data)
s <- 0.5
filtered_data$adjusted_proportion <- (filtered_data$identity_diversity_without_nans * (N - 1) + s) / N
model <- betareg(adjusted_proportion ~ Media.Trust_7, data = filtered_data)

fitted_values <- fitted(model)
residuals_values <- residuals(model)
residuals_data <- data.frame(Fitted = fitted_values, Residuals = residuals_values, Index = 1:nrow(filtered_data))
residuals_plot_3_ro <- ggplot(residuals_data, aes(x = Fitted, y = Residuals)) +
  geom_point() +
  geom_smooth(method = "loess", color = "red") +
  labs(title = "Identity Diversity without nans (Level 1)",
       x = "Fitted Values",
       y = "Residuals") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(residuals_plot_3_ro)

coefficients <- coef(model)
conf_intervals <- confint.default(model)

plot_data_identity_diversity_without_nans_ro <- data.frame(
  Variable = rownames(conf_intervals),
  Coefficient = coefficients[rownames(conf_intervals)],
  Lower_CI = conf_intervals[, 1],
  Upper_CI = conf_intervals[, 2]
)
plot_data_identity_diversity_without_nans_ro <- plot_data_identity_diversity_without_nans_ro[!rownames(plot_data_identity_diversity_without_nans_ro) %in% c("(phi)", "(Intercept)"), ]
custom_labels_identity_diversity_without_nans <- c(
  "Media.Trust_7" = "Military trust"
)



#### Information Diversity
N <- nrow(my_data)
s <- 0.5
my_data$adjusted_proportion <- (my_data$Domain_diversity * (N - 1) + s) / N
model <- betareg(adjusted_proportion ~ Ideological.Position, data = my_data)
summary(model)

coefficients <- coef(model)
conf_intervals <- confint.default(model)

plot_data_domain_diversity <- data.frame(
  Variable = rownames(conf_intervals),
  Coefficient = coefficients[rownames(conf_intervals)],
  Lower_CI = conf_intervals[, 1],
  Upper_CI = conf_intervals[, 2]
)
plot_data_domain_diversity <- plot_data_domain_diversity[!rownames(plot_data_domain_diversity) %in% c("(phi)", "(Intercept)"), ]
custom_labels_domain_diversity <- c(
  "Ideological.Position" = "Ideological position"
)

#### Check distributions 
fitted_mean <- fitted(model)

# Extract the precision parameter (phi)
precision <- model$coefficients$precision

# Calculate the shape parameters
mean_fitted_mean <- mean(fitted_mean, na.rm = TRUE)
shape1 <- mean_fitted_mean * precision
shape2 <- (1 - mean_fitted_mean) * precision

# Ensure that the adjusted_proportion has no NaNs or NAs
my_data_clean <- my_data[!is.na(my_data$adjusted_proportion) & !is.infinite(my_data$adjusted_proportion), ]

normalize_beta <- function(x) {
  dbeta(x, shape1, shape2) / 187 
}


domain_distribution_1 <- ggplot(my_data_clean, aes(x = adjusted_proportion)) +
  geom_histogram(aes(y = ..count../sum(..count..)), binwidth = 0.01, fill = "skyblue", color = "black", alpha = 1) +
  stat_function(
    fun = normalize_beta,
    color = "red",
    size = 2
  ) +
  labs(title = "Information Diversity (Level 1)",
       x = "Values",
       y = "Normalized Frequency") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        panel.grid.major = element_line(color = "grey80"),
        panel.grid.minor = element_line(color = "grey80"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))


# Display the plot
print(domain_distribution_1)
ggsave("./distribution4_level1.png", domain_distribution_1, width = 8, height = 6, units = "in", dpi = 600)

#### Check residuals
fitted_values <- fitted(model)
residuals_values <- residuals(model)
residuals_data <- data.frame(Fitted = fitted_values, Residuals = residuals_values)
residuals_plot_4 <- ggplot(residuals_data, aes(x = Fitted, y = Residuals)) +
  geom_point() +
  geom_smooth(method = "loess", color = "red") +
  labs(title = "Information Diversity (Level 1)",
       x = "Fitted Values",
       y = "Residuals") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(residuals_plot_4)


#### Check residuals (without outliers)
indexes_to_remove <- c(164, 89, 50)  
filtered_data <- my_data[-indexes_to_remove, ]
N <- nrow(filtered_data)
s <- 0.5
filtered_data$adjusted_proportion <- (filtered_data$Domain_diversity * (N - 1) + s) / N
model <- betareg(adjusted_proportion ~ Ideological.Position, data = filtered_data)

fitted_values <- fitted(model)
residuals_values <- residuals(model)
residuals_data <- data.frame(Fitted = fitted_values, Residuals = residuals_values, Index = 1:nrow(filtered_data))

# Create the residuals plot with annotations using ggrepel
residuals_plot_4_ro <- ggplot(residuals_data, aes(x = Fitted, y = Residuals)) +
  geom_point() +
  geom_smooth(method = "loess", color = "red") +
  labs(title = "Information Diversity (Level 1)",
       x = "Fitted Values",
       y = "Residuals") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(residuals_plot_4_ro)

coefficients <- coef(model)
conf_intervals <- confint.default(model)

plot_data_domain_diversity_ro <- data.frame(
  Variable = rownames(conf_intervals),
  Coefficient = coefficients[rownames(conf_intervals)],
  Lower_CI = conf_intervals[, 1],
  Upper_CI = conf_intervals[, 2]
)
plot_data_domain_diversity_ro <- plot_data_domain_diversity_ro[!rownames(plot_data_domain_diversity_ro) %in% c("(phi)", "(Intercept)"), ]
custom_labels_domain_diversity <- c(
  "Ideological.Position" = "Ideological position"
)


#### Structural Isolation
N <- nrow(my_data)
s <- 0.5
my_data$adjusted_proportion <- (my_data$Normalized_cut * (N - 1) + s) / N
model <- betareg(adjusted_proportion ~ Incivility.Perception_Impoliteness_Twitter + Gender + Religious.level, data = my_data)
summary(model)

coefficients <- coef(model)
conf_intervals <- confint.default(model)

plot_data_normalized_cut <- data.frame(
  Variable = rownames(conf_intervals),
  Coefficient = coefficients[rownames(conf_intervals)],
  Lower_CI = conf_intervals[, 1],
  Upper_CI = conf_intervals[, 2]
)
plot_data_normalized_cut <- plot_data_normalized_cut[!rownames(plot_data_normalized_cut) %in% c("(phi)", "(Intercept)"), ]
plot_data_normalized_cut$Variable <- factor(plot_data_normalized_cut$Variable, levels = rev(c("Religious.level", "Gender2", "Incivility.Perception_Impoliteness_Twitter")))

custom_labels_normalized_cut <- c(
  "Incivility.Perception_Impoliteness_Twitter" = "Incivility perception",
  "Gender2" = "Female",
  "Religious.level" = "Religious level"
)


#### Check distributions 
fitted_mean <- fitted(model)

# Extract the precision parameter (phi)
precision <- model$coefficients$precision

# Calculate the shape parameters
mean_fitted_mean <- mean(fitted_mean, na.rm = TRUE)
shape1 <- mean_fitted_mean * precision
shape2 <- (1 - mean_fitted_mean) * precision

# Ensure that the adjusted_proportion has no NaNs or NAs
my_data_clean <- my_data[!is.na(my_data$adjusted_proportion) & !is.infinite(my_data$adjusted_proportion), ]

normalize_beta <- function(x) {
  dbeta(x, shape1, shape2) / 187 
}

nc_distribution_1 <- ggplot(my_data_clean, aes(x = adjusted_proportion)) +
  geom_histogram(aes(y = ..count../sum(..count..)), binwidth = 0.01, fill = "skyblue", color = "black", alpha = 1) +
  stat_function(
    fun = normalize_beta,
    color = "red",
    size = 2
  ) +
  labs(title = "Structural Isolation (Level 1)",
       x = "Values",
       y = "Normalized Frequency") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        panel.grid.major = element_line(color = "grey80"),
        panel.grid.minor = element_line(color = "grey80"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(nc_distribution_1)
ggsave("./distribution5_level1.png", nc_distribution_1, width = 8, height = 6, units = "in", dpi = 600)


#### Check residuals
fitted_values <- fitted(model)
residuals_values <- residuals(model)
residuals_data <- data.frame(Fitted = fitted_values, Residuals = residuals_values)
residuals_plot_5 <- ggplot(residuals_data, aes(x = Fitted, y = Residuals)) +
  geom_point() +
  geom_smooth(method = "loess", color = "red") +
  labs(title = "Structural Isolation (Level 1)",
       x = "Fitted Values",
       y = "Residuals") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(residuals_plot_5)


#### Check residuals (without outliers)
indexes_to_remove <- c(150, 151) 
filtered_data <- my_data[-indexes_to_remove, ]
N <- nrow(filtered_data)
s <- 0.5
filtered_data$adjusted_proportion <- (filtered_data$Normalized_cut * (N - 1) + s) / N
model <- betareg(adjusted_proportion ~ Incivility.Perception_Impoliteness_Twitter + Gender + Religious.level, data = filtered_data)

fitted_values <- fitted(model)
residuals_values <- residuals(model)
residuals_data <- data.frame(Fitted = fitted_values, Residuals = residuals_values, Index = 1:nrow(filtered_data))

# Create the residuals plot with annotations using ggrepel
residuals_plot_5_ro <- ggplot(residuals_data, aes(x = Fitted, y = Residuals)) +
  geom_point() +
  geom_smooth(method = "loess", color = "red") +
  labs(title = "Structural Isolation (Level 1)",
       x = "Fitted Values",
       y = "Residuals") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(residuals_plot_5_ro)

coefficients <- coef(model)
conf_intervals <- confint.default(model)

plot_data_normalized_cut_ro <- data.frame(
  Variable = rownames(conf_intervals),
  Coefficient = coefficients[rownames(conf_intervals)],
  Lower_CI = conf_intervals[, 1],
  Upper_CI = conf_intervals[, 2]
)
plot_data_normalized_cut_ro <- plot_data_normalized_cut_ro[!rownames(plot_data_normalized_cut_ro) %in% c("(phi)", "(Intercept)"), ]
plot_data_normalized_cut_ro$Variable <- factor(plot_data_normalized_cut_ro$Variable, levels = rev(c("Religious.level", "Gender2", "Incivility.Perception_Impoliteness_Twitter")))

custom_labels_normalized_cut <- c(
  "Incivility.Perception_Impoliteness_Twitter" = "Incivility perception",
  "Gender2" = "Female",
  "Religious.level" = "Religious level"
)

#### Connectivity Inequality
N <- nrow(my_data)
s <- 0.5
my_data$adjusted_proportion <- (my_data$Gini * (N - 1) + s) / N
model <- betareg(adjusted_proportion ~  Age + Ideological.Position, data = my_data)
summary(model)

coefficients <- coef(model)
conf_intervals <- confint.default(model)

plot_data_gini <- data.frame(
  Variable = rownames(conf_intervals),
  Coefficient = coefficients[rownames(conf_intervals)],
  Lower_CI = conf_intervals[, 1],
  Upper_CI = conf_intervals[, 2]
)
plot_data_gini <- plot_data_gini[!rownames(plot_data_gini) %in% c("(phi)", "(Intercept)"), ]
plot_data_gini$Variable <- factor(plot_data_gini$Variable, levels = rev(c("Ideological.Position", "Age")))

custom_labels_gini <- c(
  "Age" = "Age",
  "Ideological.Position" = "Ideological position"
)


#### Check distributions 
fitted_mean <- fitted(model)

# Extract the precision parameter (phi)
precision <- model$coefficients$precision

# Calculate the shape parameters
mean_fitted_mean <- mean(fitted_mean, na.rm = TRUE)
shape1 <- mean_fitted_mean * precision
shape2 <- (1 - mean_fitted_mean) * precision

# Ensure that the adjusted_proportion has no NaNs or NAs
my_data_clean <- my_data[!is.na(my_data$adjusted_proportion) & !is.infinite(my_data$adjusted_proportion), ]

normalize_beta <- function(x) {
  dbeta(x, shape1, shape2) / 187 
}

gini_distribution_1 <- ggplot(my_data_clean, aes(x = adjusted_proportion)) +
  geom_histogram(aes(y = ..count../sum(..count..)), binwidth = 0.01, fill = "skyblue", color = "black", alpha = 1) +
  stat_function(
    fun = normalize_beta,
    color = "red",
    size = 2
  ) +
  labs(title = "Connectivity Inequality (Level 1)",
       x = "Values",
       y = "Normalized Frequency") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        panel.grid.major = element_line(color = "grey80"),
        panel.grid.minor = element_line(color = "grey80"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(gini_distribution_1)
ggsave("./distribution6_level1.png", gini_distribution_1, width = 8, height = 6, units = "in", dpi = 600)


#### Check residuals
fitted_values <- fitted(model)
residuals_values <- residuals(model)
residuals_data <- data.frame(Fitted = fitted_values, Residuals = residuals_values)
residuals_plot_6 <- ggplot(residuals_data, aes(x = Fitted, y = Residuals)) +
  geom_point() +
  geom_smooth(method = "loess", color = "red") +
  labs(title = "Connectivity Inequality (Level 1)",
       x = "Fitted Values",
       y = "Residuals") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(residuals_plot_6)


#### Check residuals (without outliers)
indexes_to_remove <- c() 
filtered_data <- my_data
N <- nrow(filtered_data)
s <- 0.5
filtered_data$adjusted_proportion <- (filtered_data$Gini * (N - 1) + s) / N
model <- betareg(adjusted_proportion ~ Age + Ideological.Position, data = filtered_data)

fitted_values <- fitted(model)
residuals_values <- residuals(model)
residuals_data <- data.frame(Fitted = fitted_values, Residuals = residuals_values, Index = 1:nrow(filtered_data))

# Create the residuals plot with annotations using ggrepel
residuals_plot_6_ro <- ggplot(residuals_data, aes(x = Fitted, y = Residuals)) +
  geom_point() +
  geom_smooth(method = "loess", color = "red") +
  labs(title = "Connectivity Inequality (Level 1)",
       x = "Fitted Values",
       y = "Residuals") +
  theme_minimal() +
  theme(panel.background = element_rect(fill = "white"),
        axis.text = element_text(color = "black", size = 20),
        axis.title = element_text(size = 28),
        plot.title = element_text(size = 28))

# Display the plot
print(residuals_plot_6_ro)


coefficients <- coef(model)
conf_intervals <- confint.default(model)

plot_data_gini_ro <- data.frame(
  Variable = rownames(conf_intervals),
  Coefficient = coefficients[rownames(conf_intervals)],
  Lower_CI = conf_intervals[, 1],
  Upper_CI = conf_intervals[, 2]
)
plot_data_gini_ro <- plot_data_gini_ro[!rownames(plot_data_gini_ro) %in% c("(phi)", "(Intercept)"), ]
plot_data_gini_ro$Variable <- factor(plot_data_gini_ro$Variable, levels = rev(c("Ideological.Position", "Age")))
custom_labels_gini <- c(
  "Age" = "Age",
  "Ideological.Position" = "Ideological position"
)


# Create regression plots 
plot1_1 <- create_plot(plot_data_overlap, custom_labels_overlap, "Level 1", x_label = "Community Overlap")
plot1_2 <- create_plot(plot_data_identity_diversity_with_nans, custom_labels_identity_diversity_with_nans, "Level 1", x_label = "Identity Diversity")
plot1_3 <- create_plot(plot_data_identity_diversity_without_nans, custom_labels_identity_diversity_without_nans, "Level 1", x_label = "Identity Diversity1")
plot1_4 <- create_plot(plot_data_domain_diversity, custom_labels_domain_diversity, "Level 1", x_label = "Information Diversity")
plot1_5 <- create_plot(plot_data_normalized_cut, custom_labels_normalized_cut, "Level 1", x_label = "Structural Isolation")
plot1_6 <- create_plot(plot_data_gini, custom_labels_gini, "Level 1", x_label = "Connectivity Inequality")

# Create regression plots for sensitivity check
plot1_1_ro <- create_plot(plot_data_overlap, custom_labels_overlap, "Level 1", x_label = "Community Overlap")
plot1_2_ro <- create_plot(plot_data_identity_diversity_with_nans_ro, custom_labels_identity_diversity_with_nans, "Level 1", x_label = "Identity Diversity")
plot1_3_ro <- create_plot(plot_data_identity_diversity_without_nans_ro, custom_labels_identity_diversity_without_nans, "Level 1", x_label = "Identity Diversity1")
plot1_4_ro <- create_plot(plot_data_domain_diversity_ro, custom_labels_domain_diversity, "Level 1", x_label = "Information Diversity")
plot1_5_ro <- create_plot(plot_data_normalized_cut_ro, custom_labels_normalized_cut, "Level 1", x_label = "Structural Isolation")
plot1_6_ro <- create_plot(plot_data_gini_ro, custom_labels_gini, "Level 1", x_label = "Connectivity Inequality")

# Create plots for distribution checks, residuals checks, and residuals checks after removing outliers
combined_distributions <- (overlap_distribution_1 + label1_distribution_1 + label2_distribution_1) / (domain_distribution_1 + nc_distribution_1 + gini_distribution_1) +
  plot_layout(guides = 'collect') +
  theme(plot.margin = margin(3, 3, 3, 3, "mm"))
ggsave("/Users/yuazhan/Downloads/SI_Fig.14_Fitted_distributions_l1.png", combined_distributions, width = 25, height = 13, units = "in", dpi = 300)

combined_residuals <- (residuals_plot_2 + residuals_plot_3 + residuals_plot_4) / (residuals_plot_5 + residuals_plot_6) +
  plot_layout(guides = 'collect') &
  theme(plot.margin = margin(3, 3, 3, 3, "mm"))
ggsave("/Users/yuazhan/Downloads/SI_Fig.18_Residuals_with_outliers_l1.png", combined_residuals, width = 25, height = 13, units = "in", dpi = 300)

combined_residuals_ro <- (residuals_plot_2_ro + residuals_plot_3_ro + residuals_plot_4_ro) / (residuals_plot_5_ro + residuals_plot_6_ro) +
  plot_layout(guides = 'collect') &
  theme(plot.margin = margin(3, 3, 3, 3, "mm"))
ggsave("/Users/yuazhan/Downloads/SI_Fig.22_Residuals_without_outliers_l1.png", combined_residuals_ro, width = 25, height = 13, units = "in", dpi = 300)


#### REPEAT THE SAME PROCEDURE FOR LEVEL 2, LEVEL 3, AND LEVEL 4

# Combine plots for all the levels (original regression plots and sensitivity check plots)
combined_plot_11 <- plot1_1 | plot2_1 | plot3_1 | plot4_1 + plot_layout(guides = 'collect')
combined_plot_22 <- plot1_2 | plot2_2 | plot3_2 | plot4_2 + plot_layout(guides = 'collect')
combined_plot_44 <- plot1_4 | plot2_4 | plot3_4 | plot4_4 + plot_layout(guides = 'collect')
combined_plot_55 <- plot1_5 | plot2_5 | plot3_5 | plot4_5 + plot_layout(guides = 'collect')
combined_plot_66 <- plot1_6 | plot2_6 | plot3_6 | plot4_6 + plot_layout(guides = 'collect')

combined_plot_11_ro <- plot1_1_ro | plot2_1_ro | plot3_1_ro | plot4_1_ro + plot_layout(guides = 'collect')
combined_plot_22_ro <- plot1_2_ro | plot2_2_ro | plot3_2_ro | plot4_2_ro + plot_layout(guides = 'collect')
combined_plot_44_ro <- plot1_4_ro | plot2_4_ro | plot3_4_ro | plot4_4_ro + plot_layout(guides = 'collect')
combined_plot_55_ro <- plot1_5_ro | plot2_5_ro | plot3_5_ro | plot4_5_ro + plot_layout(guides = 'collect')
combined_plot_66_ro <- plot1_6_ro | plot2_6_ro | plot3_6_ro | plot4_6_ro + plot_layout(guides = 'collect')

final_combined_plot <- combine_plots(
  combined_plot_11, combined_plot_22, combined_plot_44, combined_plot_55, combined_plot_66
)

# Save the final combined regression plot
ggsave("/Users/yuazhan/Downloads/Fig.6_regression results.png", final_combined_plot, width = 41, height = 64, units = "in", dpi = 300, limitsize = FALSE)

final_combined_plot_ro <- combine_plots(
  combined_plot_11_ro, combined_plot_22_ro, combined_plot_44_ro, combined_plot_55_ro, combined_plot_66_ro
)

# Save the final combined regression plot after sensitivity check
ggsave("/Users/yuazhan/Downloads/Fig.7_regression results remove outliers.png", final_combined_plot_ro, width = 41, height = 64, units = "in", dpi = 300, limitsize = FALSE)




