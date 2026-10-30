import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation
{
    id: presentation

    Timer {
        interval: 15000
        repeat: true
        running: true
        onTriggered: presentation.goToNextSlide()
    }

    Slide {
        Image {
            id: img1
            source: "slide1.png"
            width: 560; height: 300
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }
    }
    Slide {
        Image {
            id: img2
            source: "slide2.png"
            width: 560; height: 300
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }
    }
    Slide {
        Image {
            id: img3
            source: "slide3.png"
            width: 560; height: 300
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }
    }
    Slide {
        Image {
            id: img4
            source: "slide4.png"
            width: 560; height: 300
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }
    }
}
