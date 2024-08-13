# Install necessary packages if they are not already installed
if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2")
if (!requireNamespace("reshape2", quietly = TRUE)) install.packages("reshape2")

# Load the packages
library(ggplot2)
library(reshape2)
library(gridExtra)
library(grid)
library(cowplot)

# Load the data
data <- read.csv("./Data/Multidimensional_Annotation_Influencers.csv")
contingency_df <- data[c("Political.Ideology", "Campaign.Support", "Social.Identity", "Account.Type")]

# Generate all pairs of columns
column_pairs <- combn(names(contingency_df), 2, simplify = FALSE)
results <- list()

# Perform Fisher's Exact Test for each pair
for (pair in column_pairs) {
  sub_data <- contingency_df[pair]
  clean_data <- sub_data[!is.na(sub_data[[1]]) & !is.na(sub_data[[2]]) & sub_data[[1]] != "" & sub_data[[2]] != "", ]
  table_data <- table(clean_data[[1]], clean_data[[2]], useNA = "no")
  
  if (nrow(table_data) > 1) {
    test_result <- fisher.test(table_data, hybrid = TRUE, hybridPars = c(expect = 5, percent = 80, Emin = 1), 
                               simulate.p.value = TRUE, B = 10000, workspace = 200000)
    results[[paste(pair[[1]], pair[[2]], sep = "_vs_")]] <- list(table = table_data, p_value = test_result$p.value)
  } else {
    results[[paste(pair[[1]], pair[[2]], sep = "_vs_")]] <- list(table = table_data, p_value = NA)
  }
}

# Function to determine if the background color is light or dark
is_light_color <- function(color) {
  rgb <- col2rgb(color, alpha = FALSE)
  yiq <- (rgb[1,] * 0.299 + rgb[2,] * 0.587 + rgb[3,] * 0.114)
  return(yiq > 128)  # brightness threshold
}

# Function to format the title
format_title <- function(title) {
  title <- gsub("_vs_", " vs ", title)
  title <- gsub("\\.", " ", title)
  return(title)
}

plot_heatmap <- function(table, p_value, title, x_label = NULL, y_label = NULL, show_annotations = TRUE) {
  table_melted <- melt(table)
  
  # Define a color palette
  color_palette <- c("#ffffd9", "#edf8b1", "#c7e9b4", "#7fcdbb", "#2c7fb8", "#253494", "#081d58")
  deeper_palette <- scale_fill_gradientn(colors = color_palette)
  
  subtitle <- ifelse(is.na(p_value), "Fisher's p-value: NA", 
                     ifelse(p_value < 0.01, "Fisher's p-value < 0.01", "Fisher's p-value = 1.00"))
  
  p <- ggplot(table_melted, aes(x = Var2, y = Var1, fill = value)) +
    geom_tile(color = "white", size = 0.1) +
    deeper_palette +
    labs(title = format_title(title), subtitle = subtitle, x = x_label, y = y_label) +
    theme_minimal() +
    coord_fixed(ratio = 1)  
  
  if (show_annotations) {
    p <- p + geom_text(aes(label = value), size = 3, vjust = 0.5,
                       color = ifelse(is_light_color(color_palette[as.numeric(cut(table_melted$value, breaks = length(color_palette)))]), "black", "white")) +
      theme(
        axis.text.x = element_text(angle = 45, hjust = 1, size = 10),
        axis.text.y = element_text(size = 10),
        plot.title = element_text(size = 14, face = "bold", hjust = 0.5),
        plot.subtitle = element_text(size = 12, face = "italic", hjust = 0.5),
        plot.margin = margin(0.8, 0.8, 0.8, 0.8, "cm"),
        legend.position = "right"
      )
  } else {
    p <- p + theme(
      axis.text.x = element_blank(),
      axis.text.y = element_blank(),
      axis.title.x = element_blank(),
      axis.title.y = element_blank(),
      plot.title = element_blank(),
      plot.subtitle = element_blank(),
      legend.position = "none"
    )
  }
  
  return(p)
}

# Generate plots
plots <- lapply(names(results), function(x) {
  if (x == "Social.Identity_vs_Account.Type") {
    plot_heatmap(t(results[[x]]$table), results[[x]]$p_value, title = "Account.Type_vs_Social.Identity")
  } else {
    plot_heatmap(results[[x]]$table, results[[x]]$p_value, title = x)
  }
})

while (length(plots) < 6) {
  plots <- c(plots, ggplot() + theme_void())
}

# Create a grid layout with 3 rows and 2 columns
grid_layout <- grid.arrange(grobs = plots, ncol = 2, nrow = 3, heights = unit(c(1, 1, 1), "null"), widths = unit(c(1, 1), "null"))

# Save the layout
ggsave("./Plots/Fig.1_contingency_table.png", plot = grid_layout, width = 12, height = 10, dpi = 300)








#fisher.test(df,  hybrid = TRUE,
#            hybridPars = c(expect = 5, percent = 80, Emin = 1),
#            workspace = 20000000)


library(ggplot2)

wrap_labels <- function(labels, width) {
  sapply(labels, function(x) paste(strwrap(x, width = width), collapse = "\n"))
}

nature_theme <- theme(
  text = element_text(size = 20),
  axis.text.x = element_text(size = 15, angle = 45, hjust = 1),
  axis.text.y = element_text(size = 15),
  axis.title = element_text(size = 20),
  plot.title = element_text(size = 25, hjust = 0.5)
)

create_plot <- function(data, labels, title, x_label = "Coefficient", decimals = 3, label_width = 10, x_limits = c(-0.5, 0.5), x_breaks = seq(-0.5, 0.5, 0.2)) {
  data$title <- title  # Add the title as a column to the data frame
  wrapped_labels <- wrap_labels(labels, label_width)  # Wrap the labels
  
  # Ensure the wrapped labels match the variables in the data
  names(wrapped_labels) <- names(labels)
  
  ggplot(data, aes(x = Coefficient, y = Variable)) +
    geom_segment(aes(x = Lower_CI, xend = Upper_CI, y = Variable, yend = Variable), color = "black", size = 1.5) +
    geom_point(size = 3.5) +
    geom_vline(xintercept = 0, color = "red", size = 1) +
    geom_text(aes(label = round(Coefficient, decimals), x = Coefficient), vjust = -1, size = 4, color = "blue") +
    scale_y_discrete(labels = wrapped_labels) +
    scale_x_continuous(limits = x_limits, breaks = x_breaks) +  # Set x-axis limits and breaks
    labs(x = x_label, y = "") +
    theme_bw() + nature_theme +
    facet_wrap(~title)
}

plot_data_overlap <- data.frame(
  Variable = c("Satisfactory.with.Democracy", "Incivility.Perception_Impoliteness_Twitter", "Read.Watch_Twitter", "Age", "Ideological.Position"),
  Coefficient = c(0.19724571, 0.09555274, 0.07914249, 0.02662324, -0.11046817),
  Lower_CI = c(0.04348353, 0.02671211, 0.03165597, 0.01465894, -0.15355646),
  Upper_CI = c(0.35100788, 0.16439336, 0.12662901, 0.03858753, -0.06737988)
)

# Set the factor levels in reverse order to ensure the correct order in the plot
plot_data_overlap$Variable <- factor(plot_data_overlap$Variable, levels = rev(c("Ideological.Position", "Incivility.Perception_Impoliteness_Twitter", "Read.Watch_Twitter", "Age", "Satisfactory.with.Democracy")))

custom_labels_overlap <- c(
  "Satisfactory.with.Democracy" = "Democracy satisfaction",
  "Incivility.Perception_Impoliteness_Twitter" = "Incivility perception",
  "Read.Watch_Twitter" = "Twitter consumption",
  "Age" = "Age",
  "Ideological.Position" = "Ideological position"
)

# Create the plot
plot <- create_plot(plot_data_overlap, custom_labels_overlap, "Selective Exposure Indices", x_limits = c(-0.2, 0.4), x_breaks = seq(-0.2, 0.4, 0.1))

# Display the plot
print(plot)

