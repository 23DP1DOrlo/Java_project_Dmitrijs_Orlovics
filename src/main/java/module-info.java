module com.example.java_project_timer {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.desktop;


    opens com.example.java_project_timer to javafx.fxml;
    exports com.example.java_project_timer;
    module com.example.java_project_timer {
    requires java.desktop;
}
}