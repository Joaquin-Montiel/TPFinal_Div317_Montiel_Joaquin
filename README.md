# TPFinal_Div317_Montiel_Joaquin
Dragon Ball Z  Trading Card Game [TCG]

Proyecto académico desarrollado para la materia Programación I de la Universidad Tecnológica Nacional (UTN).

## 🧠 Descripción del proyecto
Juego de cartas por turnos basado en el universo Dragon Ball Z, donde el jugador se enfrenta a la computadora en una batalla de cartas.
Cada participante posee un mazo de cartas con distintos atributos (HP, ATK, DEF y bonus), los cuales determinan el desarrollo de la partida.

El objetivo del proyecto fue implementar la lógica completa del juego respetando reglas, condiciones de victoria, manejo de datos y modularización del código.
---

## ⚙️ Funcionalidades principales
- Menú principal con opciones de juego
- Ingreso de nombre del jugador
- Sistema de batalla por turnos
- Comparación de ataque entre cartas con aplicación de bonus
- Sistema de comodines:
  - **HEAL**: recuperación total de vida inicial (uso único)
  - **SHIELD**: refleja el daño al oponente (uso único)
- Cálculo dinámico de HP, ATK y DEF según las cartas utilizadas
- Sistema de puntos por manos ganadas
- Ranking de los 10 mejores puntajes
- Finalización de la partida por:
  - HP igual a 0
  - Falta de cartas
  - Tiempo agotado
---

## 🛠️ Tecnologías y conceptos aplicados
- **Lenguaje:** Python
- **Estructuras de datos:** listas, diccionarios, tuplas
- **Paradigma:** programación funcional
- **Archivos:** lectura y escritura de JSON y CSV
- **Lógica de juego:** control de estados, validaciones y reglas
- **Módulos:** uso de `random` para golpes críticos
- **Buenas prácticas:** funciones reutilizables, modularización del código y documentación
---

## 📂 Configuración del juego
Los datos del juego (configuración inicial y mazos de cartas) se leen desde archivos JSON, lo que permite modificar valores como:
- Cantidad de cartas por mazo
- Stats de las cartas
- Configuraciones generales del juego
Esto permite una mayor flexibilidad y escalabilidad del proyecto.
---

## ▶️ Cómo ejecutar el proyecto
1. Clonar el repositorio:
    - abrir el cmd/bash de su computadora y escribir el siguiente comando:
        git clone https://github.com/Joaquin-Montiel/TPFinal_Div317_Montiel_Joaquin
2. Acceder al directorio del proyecto.
3. Ejecutar el archivo principal: main.py
