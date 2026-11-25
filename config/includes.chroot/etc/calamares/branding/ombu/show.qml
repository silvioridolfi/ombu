import QtQuick 2.0;
import calamares.slideshow 1.0;

// Las diapositivas (1000x380) llenan todo el espacio de la presentación; si el área tiene otra proporción se recortan
// por los costados (el contenido está dentro de un margen seguro). Generado por tools/gen-slides.py.
Presentation
{
    id: presentation

    Timer {
        interval: 15000
        repeat: true
        running: true
        onTriggered: presentation.goToNextSlide()
    }

    Slide { Image { anchors.fill: parent; source: "slide1.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide2.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide3.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide4.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide5.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide6.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide7.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide8.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide9.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide10.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide11.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide12.png"; fillMode: Image.PreserveAspectCrop } }
    Slide { Image { anchors.fill: parent; source: "slide13.png"; fillMode: Image.PreserveAspectCrop } }
}
