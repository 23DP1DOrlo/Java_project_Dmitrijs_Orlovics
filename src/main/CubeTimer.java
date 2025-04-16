import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class CubeTimer extends Application {
    @Override
    public void start(Stage primaryStage) {
        Button btn = new Button("Старт / Стоп");
        btn.setOnAction(e -> System.out.println("Таймер нажат!"));

        StackPane root = new StackPane(btn);
        Scene scene = new Scene(root, 400, 300);

        primaryStage.setTitle("Cube Timer");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}