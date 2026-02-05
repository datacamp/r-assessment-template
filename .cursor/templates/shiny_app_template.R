# ==============================================================================
# DataCamp Shiny App Template
# ==============================================================================
#
# This template provides the foundation for building explorable exercise Shiny apps
# with DataCamp theming and required localization.
#
# REQUIREMENTS:
# - Poppins font (Google Fonts)
# - DataCamp brand colors
# - Localization with at least 2 languages
# - Language selector dropdown
#
# USAGE:
# 1. Copy this template to your app folder (e.g., apps/ch1_ex9/app.R)
# 2. Customize TRANSLATIONS for your content
# 3. Build your UI and server logic
# 4. Run with: shiny::runApp('apps/ch1_ex9')
#
# ==============================================================================

library(shiny)
library(shinyjs)
library(markdown)

# ==============================================================================
#  TRANSLATIONS (REQUIRED)
# ==============================================================================
#
# All UI text MUST be in the TRANSLATIONS list.
# Minimum: 2 languages (English + 1 other)
# Recommended: EN, ES, DE, FR
#

TRANSLATIONS <- list(
  en = list(
    flag = "🇺🇸",
    ui = list(
      title = "Application Title",
      subtitle = "Application description goes here",
      # Header elements
      header_welcome = "Welcome",
      header_status = "Status:",
      status_ready = "Ready",
      status_loading = "Loading...",
      # Buttons
      btn_submit = "Submit",
      btn_reset = "Reset",
      btn_next = "Next",
      # Common labels
      label_select = "Select an option",
      label_result = "Result",
      # Messages
      msg_success = "Great job!",
      msg_error = "Something went wrong",
      msg_loading = "Please wait..."
    ),
    content = list(
      # Add your content-specific translations here
      # e.g., questions, options, feedback text
      item_1 = "First item",
      item_2 = "Second item",
      item_3 = "Third item"
    )
  ),
  es = list(
    flag = "🇪🇸",
    ui = list(
      title = "Título de la Aplicación",
      subtitle = "La descripción de la aplicación va aquí",
      header_welcome = "Bienvenido",
      header_status = "Estado:",
      status_ready = "Listo",
      status_loading = "Cargando...",
      btn_submit = "Enviar",
      btn_reset = "Reiniciar",
      btn_next = "Siguiente",
      label_select = "Seleccione una opción",
      label_result = "Resultado",
      msg_success = "¡Muy bien!",
      msg_error = "Algo salió mal",
      msg_loading = "Por favor espere..."
    ),
    content = list(
      item_1 = "Primer elemento",
      item_2 = "Segundo elemento",
      item_3 = "Tercer elemento"
    )
  ),
  de = list(
    flag = "🇩🇪",
    ui = list(
      title = "Anwendungstitel",
      subtitle = "Anwendungsbeschreibung hier",
      header_welcome = "Willkommen",
      header_status = "Status:",
      status_ready = "Bereit",
      status_loading = "Laden...",
      btn_submit = "Absenden",
      btn_reset = "Zurücksetzen",
      btn_next = "Weiter",
      label_select = "Option auswählen",
      label_result = "Ergebnis",
      msg_success = "Gut gemacht!",
      msg_error = "Etwas ist schief gelaufen",
      msg_loading = "Bitte warten..."
    ),
    content = list(
      item_1 = "Erstes Element",
      item_2 = "Zweites Element",
      item_3 = "Drittes Element"
    )
  ),
  fr = list(
    flag = "🇫🇷",
    ui = list(
      title = "Titre de l'Application",
      subtitle = "Description de l'application ici",
      header_welcome = "Bienvenue",
      header_status = "Statut:",
      status_ready = "Prêt",
      status_loading = "Chargement...",
      btn_submit = "Soumettre",
      btn_reset = "Réinitialiser",
      btn_next = "Suivant",
      label_select = "Sélectionnez une option",
      label_result = "Résultat",
      msg_success = "Bien joué!",
      msg_error = "Quelque chose s'est mal passé",
      msg_loading = "Veuillez patienter..."
    ),
    content = list(
      item_1 = "Premier élément",
      item_2 = "Deuxième élément",
      item_3 = "Troisième élément"
    )
  )
)

# ==============================================================================
#  HELPER FUNCTIONS (REQUIRED)
# ==============================================================================

#' Get available language choices for dropdown
#' @return Named vector of language codes with flag emojis
get_language_choices <- function() {
  c("🇺🇸" = "en", "🇪🇸" = "es", "🇩🇪" = "de", "🇫🇷" = "fr")
}

#' Retrieve translation by language and path
#' @param lang Language code (e.g., "en", "es")
#' @param ... Path to translation (e.g., "ui", "title")
#' @return Translated string or NULL if not found
t <- function(lang, ...) {
  keys <- list(...)
  result <- TRANSLATIONS[[lang]]
  for (key in keys) {
    result <- result[[key]]
    if (is.null(result)) return(NULL)
  }
  result
}

# ==============================================================================
#  DATACAMP THEME CSS
# ==============================================================================

DATACAMP_CSS <- "
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* CSS Variables - DataCamp Brand Colors */
:root {
  --dc-navy: #05192d;
  --dc-navy-light: #0a2240;
  --dc-green: #03ef62;
  --dc-green-light: #65ff8f;
  --dc-green-dark: #00c74e;
  --dc-orange: #ff931e;
  --dc-red: #ff5400;
  --dc-gray-light: #f7f7fc;
  --dc-gray-border: #e8e8ea;
  --dc-text: #05192d;
  --dc-text-light: #ffffff;
  --dc-text-subtle: rgba(48, 57, 105, 0.6);
}

/* Base Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--dc-gray-light);
  color: var(--dc-text);
  line-height: 1.6;
  min-height: 100vh;
}

.container-fluid {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Header */
.app-header {
  background: var(--dc-navy);
  color: var(--dc-text-light);
  padding: 24px 30px;
  border-radius: 12px 12px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content {
  flex: 1;
}

.app-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 4px 0;
}

.app-subtitle {
  font-size: 1rem;
  opacity: 0.85;
  margin: 0;
  font-weight: 400;
}

/* Language Selector */
.language-selector {
  margin-left: 20px;
}

.language-selector select,
.language-selector .selectize-input {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  font-family: 'Poppins', sans-serif;
  transition: all 0.2s ease;
}

.language-selector select:hover,
.language-selector .selectize-input:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: var(--dc-green);
}

.language-selector select:focus {
  outline: none;
  border-color: var(--dc-green);
}

.language-selector select option {
  background: var(--dc-navy);
  color: white;
}

/* Main Content Area */
.main-content {
  background: white;
  border-radius: 0 0 12px 12px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(5, 25, 45, 0.08);
}

/* Cards */
.card {
  background: white;
  border: 1px solid var(--dc-gray-border);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(5, 25, 45, 0.1);
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--dc-navy);
  margin-bottom: 16px;
}

/* Buttons */
.btn-dc-primary {
  background: var(--dc-green);
  color: var(--dc-navy);
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Poppins', sans-serif;
}

.btn-dc-primary:hover {
  background: var(--dc-green-dark);
  transform: translateY(-1px);
}

.btn-dc-secondary {
  background: white;
  color: var(--dc-red);
  border: 2px solid var(--dc-red);
  padding: 10px 22px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Poppins', sans-serif;
}

.btn-dc-secondary:hover {
  background: var(--dc-red);
  color: white;
}

/* Status Indicator */
.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-dot.ready {
  background: var(--dc-green);
}

.status-dot.loading {
  background: var(--dc-orange);
  animation: pulse 1.5s infinite;
}

.status-dot.error {
  background: var(--dc-red);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Form Elements */
.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--dc-navy);
}

.form-control {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--dc-gray-border);
  border-radius: 8px;
  font-size: 1rem;
  font-family: 'Poppins', sans-serif;
  transition: border-color 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--dc-green);
}

/* Warning Banner */
.warning-banner {
  background: #fffbf3;
  border-left: 4px solid var(--dc-orange);
  padding: 16px 20px;
  margin-bottom: 20px;
  border-radius: 0 8px 8px 0;
}

.warning-banner strong {
  color: var(--dc-navy);
  font-weight: 600;
}

/* Success Message */
.success-message {
  background: rgba(3, 239, 98, 0.1);
  border: 1px solid rgba(3, 239, 98, 0.3);
  border-radius: 8px;
  padding: 16px 20px;
  color: var(--dc-navy);
}

.success-message strong {
  color: var(--dc-green-dark);
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fadeIn 0.4s ease-out;
}

/* Responsive */
@media (max-width: 768px) {
  .app-header {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .language-selector {
    margin-left: 0;
  }
  
  .app-title {
    font-size: 1.5rem;
  }
}
"

# ==============================================================================
#  UI
# ==============================================================================

ui <- fluidPage(
  useShinyjs(),
  
  # Head - Styles and Meta
  tags$head(
    tags$meta(charset = "UTF-8"),
    tags$meta(name = "viewport", content = "width=device-width, initial-scale=1.0"),
    tags$style(HTML(DATACAMP_CSS))
  ),
  
  # Main Container
  div(class = "container-fluid",
      
      # Header with Language Selector
      div(class = "app-header",
          div(class = "header-content",
              uiOutput("title_ui"),
              uiOutput("subtitle_ui")
          ),
          div(class = "language-selector",
              selectInput(
                "language",
                label = NULL,
                choices = get_language_choices(),
                selected = "en"
              )
          )
      ),
      
      # Main Content
      div(class = "main-content",
          
          # Warning Banner (optional - remove if not needed)
          div(class = "warning-banner",
              tags$strong("Training Mode: "),
              "This is a demonstration application for educational purposes."
          ),
          
          # Your content goes here
          div(class = "card",
              div(class = "card-title", "Getting Started"),
              p("Replace this content with your application logic."),
              p("Use the language selector in the header to test translations.")
          ),
          
          # Example: Dynamic content based on language
          uiOutput("content_ui"),
          
          # Example: Action buttons
          div(style = "margin-top: 20px;",
              actionButton("btn_action", 
                           uiOutput("btn_text", inline = TRUE), 
                           class = "btn-dc-primary"),
              actionButton("btn_reset", 
                           uiOutput("btn_reset_text", inline = TRUE), 
                           class = "btn-dc-secondary",
                           style = "margin-left: 10px;")
          )
      )
  )
)

# ==============================================================================
#  SERVER
# ==============================================================================

server <- function(input, output, session) {
  
  # Reactive values for state management
  state <- reactiveValues(
    status = "ready"
  )
  
  # ----- UI OUTPUTS (Localized) -----
  
  output$title_ui <- renderUI({
    tags$h1(class = "app-title", t(input$language, "ui", "title"))
  })
  
  output$subtitle_ui <- renderUI({
    tags$p(class = "app-subtitle", t(input$language, "ui", "subtitle"))
  })
  
  output$btn_text <- renderUI({
    t(input$language, "ui", "btn_submit")
  })
  
  output$btn_reset_text <- renderUI({
    t(input$language, "ui", "btn_reset")
  })
  
  output$content_ui <- renderUI({
    lang <- input$language
    
    div(class = "card fade-in",
        div(class = "card-title", t(lang, "ui", "label_select")),
        tags$ul(
          tags$li(t(lang, "content", "item_1")),
          tags$li(t(lang, "content", "item_2")),
          tags$li(t(lang, "content", "item_3"))
        )
    )
  })
  
  # ----- EVENT HANDLERS -----
  
  observeEvent(input$btn_action, {
    # Handle primary action
    state$status <- "loading"
    
    # Simulate async operation
    shinyjs::delay(1000, {
      state$status <- "ready"
      showNotification(
        t(input$language, "ui", "msg_success"),
        type = "message"
      )
    })
  })
  
  observeEvent(input$btn_reset, {
    # Handle reset
    state$status <- "ready"
    showNotification(
      "Reset complete",
      type = "default"
    )
  })
  
  # Reset state on language change (optional)
  observeEvent(input$language, {
    # Clear any language-specific state if needed
  })
}

# ==============================================================================
#  RUN APP
# ==============================================================================

shinyApp(ui, server)
