library(shiny)
library(VariantAnnotation)
library(DT)
library(rmarkdown)

ui <- fluidPage(
  titlePanel("NGS Variant Summary Tool"),
  sidebarLayout(
    sidebarPanel(
      fileInput("vcf_file", "Upload VCF File (.vcf)", accept = ".vcf"),
      actionButton("analyze_btn", "Analyze & Generate Report")
    ),
    mainPanel(
      DTOutput("summary_table"),
      downloadButton("download_report", "Download PDF Report")
    )
  )
)

server <- function(input, output) {
  vcf_data <- eventReactive(input$analyze_btn, {
    req(input$vcf_file)
    vcf <- readVcf(input$vcf_file$datapath, "hg19")
    ti <- sum(isSNV(vcf))
    tv <- nrow(vcf) - ti
    ratio <- if (tv > 0) round(ti / tv, 2) else NA
    data.frame(
      Total_Variants = nrow(vcf),
      SNVs = ti,
      Indels = sum(isIndel(vcf)),
      TiTv_Ratio = ratio
    )
  })

  output$summary_table <- renderDT({
    req(vcf_data())
    datatable(vcf_data())
  })

  output$download_report <- downloadHandler(
    filename = function() { "variant_report.pdf" },
    content = function(file) {
      rmarkdown::render("report_template.Rmd",
                        output_file = file,
                        params = list(summary = vcf_data()),
                        envir = new.env(parent = globalenv()))
    }
  )
}

shinyApp(ui, server)
