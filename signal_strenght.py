import ROOT
import os

# Function to load histograms from multiple ROOT files
def load_histograms(file_list, hist_name):
    """
    Load and combine histograms from multiple ROOT files.

    Args:
        file_list (list of str): List of ROOT file paths.
        hist_name (str): Name of the histogram to extract.

    Returns:
        ROOT.TH1F: Combined histogram from all files.
    """
    combined_hist = None

    for file_name in file_list:
        file = ROOT.TFile.Open(file_name)
        if not file or file.IsZombie():
            print(f"Error: Unable to open {file_name}")
            continue

        hist = file.Get(hist_name)
        if not hist:
            print(f"Error: Histogram {hist_name} not found in {file_name}")
            continue

        if combined_hist is None:
            combined_hist = hist.Clone(f"combined_{hist_name}")
            combined_hist.SetDirectory(0)
        else:
            combined_hist.Add(hist)

        file.Close()

    return combined_hist

# Function to define the Double-Sided Crystal Ball (DSCB) function
You said:
sn-article.pdf
PDF
Del reporte que te compartí quiero que me expliques de forma detallada cómo hacen el cálculo del signal strenght, me parece que empieza la explicación desde el punto 5.3 que se encuentra en la página 15 del PDF. quiero todos los detalles que pueda ofrecer el paper para este proposito
ChatGPT said:
ChatGPT

El cálculo de la signal strength en el reporte (sección 5.3) se lleva a cabo mediante un ajuste simultáneo de máxima verosimilitud (maximum likelihood) sobre la distribución de la masa de retroceso (recoil mass) en las diferentes categorías de eventos clasificados según los modos de desintegración del bosón de Higgs. A continuación, explico el proceso detalladamente:
1. Clasificación de eventos

Antes de realizar el ajuste, los eventos se agrupan en cinco categorías según el tipo de desintegración del Higgs:

    H→bbˉH→bbˉ
    H→ccˉH→ccˉ
    H→ggH→gg
    H→ssˉH→ssˉ
    Otras desintegraciones.

Estas categorías se obtienen utilizando una red neuronal que clasifica los eventos basándose en variables discriminantes, como los valores de los algoritmos de flavour tagging y características cinemáticas como la masa invariante de los jets.
2. Ajuste de máxima verosimilitud

El ajuste se realiza sobre la distribución de la masa de retroceso (mrecoilmrecoil​) en el intervalo de 120–140 GeV, con bins de 0.25 GeV. El procedimiento considera tanto las contribuciones de señal como las de fondo.
a) Construcción de la función de verosimilitud

La verosimilitud global es un producto de las funciones de verosimilitud para cada categoría. En cada categoría:

    La probabilidad de observar un número de eventos en un bin específico se modela con una distribución de Poisson.
    Los eventos esperados en cada bin son la suma de los contribuyentes de señal y fondo.

b) Modelado del fondo

    El fondo total en una categoría es un parámetro libre del ajuste.
    La distribución del fondo en mrecoilmrecoil​ se modela con una función polinómica de primer grado (lineal), cuyo parámetro de pendiente es otro parámetro libre.

c) Modelado de la señal

    La distribución de mrecoilmrecoil​ para la señal se modela mediante una función Crystall Ball de doble lado (DSCB). Esta función tiene un núcleo gaussiano y colas tipo power-law a ambos lados.
    Los parámetros que caracterizan las colas (αL,αR,nL,nRαL​,αR​,nL​,nR​) se fijan en el ajuste para evitar inestabilidades, ya que la relación señal-fondo (S/BS/B) es baja en las regiones de las colas.
    La posición del pico se modela como la masa del Higgs más un pequeño desplazamiento debido a efectos de reconstrucción.
    La anchura y el desplazamiento del pico son parámetros flotantes.

3. Parámetros de interés (POIs)

Se consideran configuraciones con diferentes números de POIs (parámetros de interés):

    3 POIs: Se ajustan las signal strengths (μμ) para H→bbˉ,H→ccˉ,H→ggH→bbˉ,H→ccˉ,H→gg, mientras que las de H→ssˉH→ssˉ y otras desintegraciones se fijan a sus valores predichos por el Modelo Estándar (SM).
    4 POIs: Se ajusta μμ para H→bbˉ,H→ccˉ,H→ggH→bbˉ,H→ccˉ,H→gg, y H→otherH→other o H→ssˉH→ssˉ, dejando fija la otra.
    5 POIs: Todas las signal strengths son flotantes.

4. Resultados esperados

Los ajustes se realizan utilizando muestras de Asimov generadas a partir de los valores nominales de los modelos de señal y fondo. Las incertidumbres estadísticas esperadas para los parámetros de interés son las siguientes (5 POIs):

    H→bbˉH→bbˉ: 0.81%
    H→ccˉH→ccˉ: 4.93%
    H→ggH→gg: 2.73%
    H→ssˉH→ssˉ: 410%
    H→otherH→other: 2.19%

El ajuste muestra que la señal H→bbˉH→bbˉ tiene una alta precisión debido a su gran relación S/BS/B. En contraste, H→ssˉH→ssˉ tiene una gran incertidumbre, reflejando la dificultad de medir este canal raro.

Si tienes dudas adicionales o necesitas más detalles, ¡puedo profundizar!
You said:
profundiza aún más y quiero que me expliques más a fondo que es la m_recoil, qué es la máxima verosimilitud,  qué es Crystall Ball de doble lado (DSCB), qué son las colas tipo power-law y qué son los párametros POIs
ChatGPT said:
ChatGPT

¡Claro! Vamos a desglosar cada concepto en detalle para que tengas una comprensión más profunda.
1. Masa de Retroceso (mrecoilmrecoil​)

La masa de retroceso (mrecoilmrecoil​) es una cantidad que se utiliza para identificar y analizar partículas que no se detectan directamente. En este caso, se utiliza para estudiar el bosón de Higgs producido junto con un bosón ZZ (proceso e+e−→ZHe+e−→ZH).
Definición:
mrecoil2=(s−EZ)2−∣p⃗Z∣2
mrecoil2​=(s
​−EZ​)2−∣p
​Z​∣2

    ss

​: Energía en el centro de masas de la colisión (∼240 GeV∼240GeV).
EZEZ​: Energía del bosón ZZ reconstruido a partir de sus productos de desintegración (por ejemplo, Z→ℓ+ℓ−Z→ℓ+ℓ−).
p⃗Zp

    ​Z​: Momento del bosón ZZ.

Intuición:

Cuando el bosón ZZ es identificado y sus propiedades se miden con precisión, el mrecoilmrecoil​ permite inferir la masa del sistema restante, que debería corresponder a la masa del bosón de Higgs (∼125 GeV∼125GeV) si este fue producido.
Uso:

La distribución de mrecoilmrecoil​ tiene un pico alrededor de 125 GeV para eventos con ZHZH, lo que ayuda a discriminar la señal de fondo.
2. Máxima Verosimilitud

La máxima verosimilitud es un método estadístico usado para ajustar modelos a los datos observados y estimar parámetros. En este caso, se aplica para ajustar la señal y el fondo en la distribución mrecoilmrecoil​.
Concepto básico:

    La verosimilitud (LL) mide qué tan probable es observar los datos dados ciertos parámetros del modelo.
    El método de máxima verosimilitud busca los valores de los parámetros que maximizan esta probabilidad.

En este análisis:

    Para cada categoría de eventos (por ejemplo, H→bbˉH→bbˉ), se construye una función de verosimilitud basada en el conteo de eventos en cada bin de mrecoilmrecoil​. La función global es el producto de las verosimilitudes individuales para cada bin.
    La verosimilitud incluye:
        Contribuciones de señal (modeladas por la distribución DSCB).
        Contribuciones de fondo (modeladas por una función lineal).
    Los parámetros ajustados son las signal strengths (μμ) y los parámetros del modelo de fondo.

3. Crystall Ball de Doble Lado (DSCB)

La función Crystall Ball de doble lado (Double-Sided Crystal Ball, DSCB) es una función ampliamente utilizada en física de partículas para modelar distribuciones con un núcleo gaussiano y colas largas.
Componentes:

    Núcleo gaussiano: Representa el comportamiento central de la distribución, donde los eventos están concentrados.
    f(x)=e−(x−μ)22σ2,para ∣x−μ∣≤αLσ o αRσ
    f(x)=e−2σ2(x−μ)2​,para ∣x−μ∣≤αL​σ o αR​σ
        μμ: Posición del pico central (en este caso, cerca de la masa del Higgs, 125 GeV).
        σσ: Ancho de la distribución.

    Colas tipo power-law: Manejan las desviaciones fuera del núcleo gaussiano, modelando eventos en las regiones extremas.
    f(x)∝(1+∣x−μ∣nσ)−n,para ∣x−μ∣>αLσ o αRσ
    f(x)∝(1+nσ∣x−μ∣​)−n,para ∣x−μ∣>αL​σ o αR​σ
        nn: Parámetro que controla qué tan rápido decrece la cola (caída más lenta que una Gaussiana pura).
        αL,αRαL​,αR​: Límite entre el núcleo y la cola en los lados izquierdo y derecho.

Intuición:

El DSCB captura bien la física de las señales, donde el núcleo representa reconstrucciones precisas y las colas incluyen efectos de resolución o procesos poco comunes.
4. Colas tipo Power-Law

Las colas tipo power-law son una forma de modelar las desviaciones significativas de los valores centrales en una distribución. Se caracterizan por decrecer más lentamente que las colas de una distribución gaussiana. Matemáticamente:
f(x)∝(1+∣x−μ∣nσ)−n
f(x)∝(1+nσ∣x−μ∣​)−n

    Usos en física:
        Modelar eventos raros o efectos instrumentales en los bordes de una distribución.
        Capturar efectos de reconstrucción en los extremos de la distribución de masas, como en mrecoilmrecoil​.

5. Parámetros de Interés (POIs)

Los POIs (Parameters of Interest) son los parámetros principales que se quieren estimar en un ajuste estadístico.
En este análisis:

Los POIs son las signal strengths (μμ), que representan la relación entre el rendimiento observado de un canal de desintegración y su valor esperado según el Modelo Estándar:
μXX=σXX⋅BXXσXXSM⋅BXXSM
μXX​=σXXSM​⋅BXXSM​σXX​⋅BXX​​

    μXX=1μXX​=1: Coincide con la predicción del Modelo Estándar.
    μXX≠1μXX​=1: Indicaría nueva física o desviaciones del Modelo Estándar.

Configuraciones de POIs en este estudio:

    3 POIs:
        μbb,μcc,μggμbb​,μcc​,μgg​ flotantes.
        μss,μotherμss​,μother​ fijas al valor del SM.
    4 POIs:
        Agrega μotherμother​ o μssμss​ como flotante.
    5 POIs:
        Todos los parámetros (μbb,μcc,μgg,μss,μotherμbb​,μcc​,μgg​,μss​,μother​) son flotantes.

Conclusión

El análisis utiliza herramientas avanzadas de ajuste estadístico, distribuciones modelo (como DSCB) y conceptos como mrecoilmrecoil​ para medir con alta precisión los modos de desintegración del Higgs. Esto permite probar las predicciones del Modelo Estándar y buscar señales de nueva física. ¿Te gustaría que amplíe alguno de estos puntos aún más?
You said:
absolutamente toda la información que me haz proporcionado en este chat, quiero que las hagas diapositivas en latex para que las copie en overleaf, quiero que sean en inglés y sean en demasía explicativas, nada redundantes, claras y precisas.
ChatGPT said:
ChatGPT

Aquí tienes un código en LaTeX que genera diapositivas utilizando el paquete beamer. He estructurado las diapositivas con títulos claros, información concisa y detalles bien organizados. Las diapositivas están en inglés y diseñadas para ser explicativas sin redundancia. Puedes copiar este código en Overleaf.

El código LaTeX ha sido preparado en un formato claro y explicativo para tu presentación en Overleaf. Si necesitas ajustes o quieres agregar más contenido, no dudes en pedírmelo.
You said:
quiero que agregues la siguiente información: "1. Clasificación de eventos

Antes de realizar el ajuste, los eventos se agrupan en cinco categorías según el tipo de desintegración del Higgs:

    H→bbˉH→bbˉ
    H→ccˉH→ccˉ
    H→ggH→gg
    H→ssˉH→ssˉ
    Otras desintegraciones.

Estas categorías se obtienen utilizando una red neuronal que clasifica los eventos basándose en variables discriminantes, como los valores de los algoritmos de flavour tagging y características cinemáticas como la masa invariante de los jets.
2. Ajuste de máxima verosimilitud

El ajuste se realiza sobre la distribución de la masa de retroceso (mrecoilmrecoil​) en el intervalo de 120–140 GeV, con bins de 0.25 GeV. El procedimiento considera tanto las contribuciones de señal como las de fondo.
a) Construcción de la función de verosimilitud

La verosimilitud global es un producto de las funciones de verosimilitud para cada categoría. En cada categoría:

    La probabilidad de observar un número de eventos en un bin específico se modela con una distribución de Poisson.
    Los eventos esperados en cada bin son la suma de los contribuyentes de señal y fondo.

b) Modelado del fondo

    El fondo total en una categoría es un parámetro libre del ajuste.
    La distribución del fondo en mrecoilmrecoil​ se modela con una función polinómica de primer grado (lineal), cuyo parámetro de pendiente es otro parámetro libre.

c) Modelado de la señal

    La distribución de mrecoilmrecoil​ para la señal se modela mediante una función Crystall Ball de doble lado (DSCB). Esta función tiene un núcleo gaussiano y colas tipo power-law a ambos lados.
    Los parámetros que caracterizan las colas (αL,αR,nL,nRαL​,αR​,nL​,nR​) se fijan en el ajuste para evitar inestabilidades, ya que la relación señal-fondo (S/BS/B) es baja en las regiones de las colas.
    La posición del pico se modela como la masa del Higgs más un pequeño desplazamiento debido a efectos de reconstrucción.
    La anchura y el desplazamiento del pico son parámetros flotantes."

quiero que vaya antes de la slide 2: recoil Mass.

de igual modo quiero que sea en inglés
ChatGPT said:
ChatGPT

He añadido una diapositiva detallada sobre la clasificación de eventos y el ajuste de máxima verosimilitud antes de la diapositiva sobre la masa de retroceso. Si necesitas más ajustes o contenido adicional, házmelo saber.
You said:
esta parte: "% Slide 2: Event Classification and Maximum Likelihood Fit
\begin{frame}{Event Classification and Maximum Likelihood Fit}
    \begin{itemize}
        \item \textbf{Event Classification:}
        \begin{itemize}
            \item Events are grouped into five categories based on Higgs decay modes:
            \begin{itemize}
                \item $H \to b\bar{b}$
                \item $H \to c\bar{c}$
                \item $H \to gg$
                \item $H \to s\bar{s}$
                \item Other decays.
            \end{itemize}
            \item Categories are determined using a neural network trained on discriminative variables:
            \begin{itemize}
                \item Flavor tagging algorithm scores.
                \item Kinematic features such as invariant mass of jets.
            \end{itemize}
        \end{itemize}
        \item \textbf{Maximum Likelihood Fit:}
        \begin{itemize}
            \item Performed on the recoil mass ($m_{\text{recoil}}$) distribution in the range 120–140 GeV with 0.25 GeV bins.
            \item Considers both signal and background contributions.
        \end{itemize}
        \item \textbf{Likelihood Function Construction:}
        \begin{itemize}
            \item Global likelihood is a product of likelihoods for each category.
            \item In each category:
            \begin{itemize}
                \item Probability of observing events in a specific bin is modeled with a Poisson distribution.
                \item Expected events in each bin are the sum of signal and background contributions.
            \end{itemize}
        \end{itemize}
        \item \textbf{Background Modeling:}
        \begin{itemize}
            \item Total background in a category is a free parameter in the fit.
            \item Background distribution in $m_{\text{recoil}}$ is modeled with a first-degree polynomial (linear function).
        \end{itemize}
        \item \textbf{Signal Modeling:}
        \begin{itemize}
            \item Signal $m_{\text{recoil}}$ distribution is modeled using a Double-Sided Crystal Ball (DSCB) function:
            \begin{itemize}
                \item Gaussian core with power-law tails on both sides.
                \item Tail parameters ($\alpha_L, \alpha_R, n_L, n_R$) are fixed to avoid instabilities due to low $S/B$ in the tails.
            \end{itemize}
            \item Peak position modeled as the Higgs mass plus a small shift due to reconstruction effects.
            \item Width and peak shift are floating parameters.
        \end{itemize}
    \end{itemize}
\end{frame}"

quiero que la distribuyas en más diapositivas, en una sola simplemente no cabe y es demasiada información, considera que sean 3 o 4
ChatGPT said:
ChatGPT

He dividido la diapositiva de clasificación de eventos y ajuste de máxima verosimilitud en cuatro diapositivas para que la información sea más clara y manejable. Si necesitas ajustes adicionales o sugerencias, házmelo saber.
You said:
aquí tengo una duda: este valor "H→ssˉ: 410%"

si es 410%, sólo quiero un sí o un no
ChatGPT said:
ChatGPT

Sí.
You said:
vale, ya que conocemos cuál es el método que se emplea para el signal strenght me gustaría saber en qué parte de mi analisis de mis datos lo debería hacer, sería despues de que ya analice mis datos y obtengo mis archivos root con aquellos eventos que ya cumplieron con los cortes que requiero, b-tagging, etc, O debería de ser a la par que se ejecutan los cortes?

ChatGPT said:
ChatGPT

El cálculo del signal strength (μμ) es un paso que normalmente se realiza después de haber aplicado los cortes y preselecciones necesarias a los datos y haber generado los archivos ROOT con los eventos seleccionados. A continuación, te explico por qué y cómo encaja en tu flujo de análisis:
Por qué hacerlo después de aplicar los cortes

    Datos limpios y preprocesados:
        Antes de calcular el signal strength, es fundamental tener un conjunto de datos limpio que cumpla con todos los criterios de selección, como los cortes cinemáticos y el b-tagging. Esto asegura que las muestras utilizadas sean representativas y que se reduzcan las contribuciones del fondo.

    Minimización de complejidad:
        Realizar los cortes y el cálculo del signal strength a la par sería innecesariamente complicado. Separar los pasos permite un control más claro del flujo de trabajo y una validación más sencilla en cada etapa.

    Separación de la física y la estadística:
        Los cortes y selecciones son pasos físicos que preparan tus datos, mientras que el cálculo del signal strength es una técnica estadística que requiere modelos ajustados (como el ajuste por máxima verosimilitud). Es más eficiente realizarlos como procesos separados.

Cómo hacerlo después de los cortes

    Generación de muestras de señal y fondo:
        Tus archivos ROOT ya contendrán los eventos seleccionados para la señal y el fondo, tras aplicar los cortes y el b-tagging.

    Construcción de distribuciones observables:
        A partir de tus datos seleccionados, genera las distribuciones relevantes (como la masa de retroceso mrecoilmrecoil​) para cada categoría de eventos.

    Modelado de señal y fondo:
        Ajusta los modelos de señal (por ejemplo, DSCB) y fondo (por ejemplo, función polinómica lineal) a las distribuciones observadas.

    Ajuste de máxima verosimilitud:
        Realiza el ajuste simultáneo para las categorías, obteniendo el valor del signal strength (μμ) y sus incertidumbres.

Casos en los que podrías considerar hacerlo en paralelo

En ciertos análisis, podrías implementar los cortes y el cálculo del signal strength de manera integrada si:

    Cortes adaptativos:
        Estás explorando cortes variables (por ejemplo, diferentes valores de bb-tagging) y necesitas optimizar el signal strength en tiempo real.

    Análisis automatizados:
        Si el cálculo del signal strength es parte de una optimización más amplia, como un análisis multivariable (MVA) donde los cortes y ajustes se combinan en un flujo de trabajo.

En estos casos, los cortes se parametrizan y el cálculo del signal strength se ejecuta en cada iteración del análisis.
Recomendación

Para la mayoría de los casos, incluyendo tu análisis, lo ideal es:

    Primero, realizar todos los cortes y guardar los eventos seleccionados en archivos ROOT.
    Después, utilizar estos datos procesados para calcular el signal strength mediante un ajuste estadístico.

Este enfoque es modular, más fácil de depurar y sigue el flujo lógico de los análisis de física de partículas. ¿Te gustaría que te ayude a estructurar este flujo de análisis o con el código para el ajuste?
You said:
vale, entonces tendría que hacer un nuevo programa para este análisis?
habrá algún paquete en el FCC Framework?
Cabe mencionar que las variables que cuentan mis archivos root finales son missingEnergy_energy, missing_p, cosTheta_miss, jj_m (masa invariante de los jets), y scoresum.

en base a estas variables cómo podríamos construir un programa para calcular el signal strenght del mismo modo que la colaboración del FCC en el paper que te compartí y ya hicimos diapositivas
ChatGPT said:
ChatGPT

Sí, necesitarás un programa adicional para realizar el análisis de signal strength, ya que implica procesos estadísticos y ajustes que generalmente no están integrados directamente en el flujo principal de análisis de eventos. En el contexto del FCC Framework, existen herramientas y ejemplos que puedes aprovechar para construir este programa, y podemos diseñar uno basado en las variables que mencionaste.
Paquetes relevantes en el FCC Framework

El FCC Framework tiene módulos que te pueden ayudar con el análisis estadístico. Dos herramientas útiles son:

    pyhf (HistFactory en Python):
        Permite realizar ajustes de máxima verosimilitud basados en histogramas, siguiendo un enfoque modular y compatible con ROOT.
        Es especialmente útil si ya tienes las distribuciones relevantes (como mrecoilmrecoil​).

    ROOT y RooFit/RooStats:
        ROOT incluye herramientas para ajustes personalizados y análisis estadístico.
        RooFit y RooStats permiten definir modelos como el DSCB y ajustar parámetros de interés (μμ, etc.).

Plan del programa

A continuación, te propongo un esquema general para calcular el signal strength utilizando las variables de tus archivos ROOT finales:
1. Entrada de datos

    Carga los archivos ROOT con las variables:
        missingEnergy_energy
        missing_p
        cosTheta_miss
        jj_m (masa invariante de los jets)
        scoresum

2. Construcción de histogramas observables

    Crea histogramas de las variables relevantes, por ejemplo:
        Para mrecoilmrecoil​: Calcula mrecoil=s−jjmmrecoil​=s

        ​−jjm​ (o una definición similar si corresponde).
        Para el fondo: Genera un histograma similar usando muestras de fondo.

3. Modelado de señal y fondo

    Define un modelo de señal usando una función DSCB para mrecoilmrecoil​.
    Modela el fondo con una función polinómica (lineal o de grado 2).

4. Ajuste de máxima verosimilitud

    Utiliza un paquete como RooFit o pyhf para realizar un ajuste conjunto sobre los histogramas de señal y fondo.
    Estima el signal strength (μμ) y sus incertidumbres.

5. Salida de resultados

    Reporta:
        El valor estimado de μμ.
        La bondad del ajuste (por ejemplo, χ2/ndfχ2/ndf o pp-valor).
        Las distribuciones ajustadas (histogramas superpuestos de señal, fondo y datos).

Ejemplo en Pseudo-Código

Aquí te dejo un esquema simplificado del programa que podríamos construir:

import ROOT

# 1. Cargar los archivos ROOT
file = ROOT.TFile("final_data.root")
tree = file.Get("events")

# 2. Construir histogramas
h_signal = ROOT.TH1F("h_signal", "Signal Model", 80, 120, 140)  # Histogram for m_recoil
h_background = ROOT.TH1F("h_background", "Background Model", 80, 120, 140)

# Llenar histogramas con los datos
for event in tree:
    m_recoil = calculate_m_recoil(event.jj_m, event.missingEnergy_energy)  # Define this function
    if is_signal_event(event):  # Define selection for signal
        h_signal.Fill(m_recoil)
    else:
        h_background.Fill(m_recoil)

# 3. Modelar señal y fondo
from ROOT import RooRealVar, RooDataHist, RooFit, RooArgList, RooAddPdf
m_recoil = RooRealVar("m_recoil", "Recoil Mass", 120, 140)
signal_model = define_dscb_model(m_recoil)  # Define a Double-Sided Crystal Ball function
background_model = define_polynomial_model(m_recoil)  # Define linear/poly background

# Crear datos para ajuste
data_signal = RooDataHist("data_signal", "Signal Data", RooArgList(m_recoil), h_signal)
data_background = RooDataHist("data_background", "Background Data", RooArgList(m_recoil), h_background)

# Ajuste conjunto
model = RooAddPdf("model", "Signal + Background", RooArgList(signal_model, background_model))
result = model.fitTo(data_signal, RooFit.Save())

# 4. Imprimir resultados
result.Print("v")

Diseño del ajuste

Basándonos en el paper, el programa debe incluir:

    Corte predefinido: Seleccionar los eventos basados en scoresumscoresum, cos⁡thetamisscosthetamiss​, etc.
    Distribuciones:
        Construir mrecoilmrecoil​.
        Asegurar que las muestras de señal y fondo estén bien separadas.
    Función de ajuste:
        Utilizar el DSCB para la señal.
        Un polinomio lineal para el fondo.

¿Qué puedo ayudarte a implementar?

Puedo preparar:

    Código detallado en Python usando ROOT y RooFit.
    Un ejemplo más específico basado en tus datos ROOT.
    **Asesoría para integrar herramientas como pyhf o RooStats`.

¿Te gustaría que comencemos con algún paso en particular? 😊
You said:
quiero el codigo detallado y completo en python, además te menciono que son varios archivos root que quiero analizar, 2 para la señal y 5 para el background, además que la estructura del archivo root es que no tiene arbol, ni ramas, directamente al abrir el archivo root están los histogramas con los nombres de las variables (que son exactamente los que te proporcioné)
ChatGPT said:
ChatGPT

Gracias por la aclaración. Con esta información, diseñaré un programa completo en Python que analice varios archivos ROOT de señal y fondo, lea los histogramas directamente desde los archivos y realice el cálculo del signal strength siguiendo el método del ajuste por máxima verosimilitud con RooFit de ROOT.

El programa manejará múltiples archivos, combinará los histogramas y ajustará un modelo de señal (DSCB) y fondo (función polinómica). Aquí está el código detallado:

El código está listo para manejar múltiples archivos ROOT de señal y fondo, cargar los histogramas especificados, combinarlos y realizar el ajuste del signal strength usando un modelo compuesto de señal (DSCB) y fondo (polinomio lineal). Si necesitas ajustes o explicaciones adicionales sobre el código, ¡avísame!
You said:
estos serían los archivos de señal: ""wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365_vbf"" y esto para el bg: ""ZZ": ["p8_ee_ZZ_ecm365"], "WW": ["p8_ee_WW_ecm365"], "tt": ["p8_ee_tt_ecm365"], "ZH": ["wzp6_ee_numunumuH_Hbb_ecm365"]"

quiero que tenga una dirección de output outdir         = '/eos/user/f/fdmartin/FCC365_histograms/signal_strenght' y de input
ChatGPT said:
ChatGPT

He actualizado el código para que use las rutas específicas de entrada y salida que proporcionaste. Los archivos de señal y fondo se cargan desde el directorio de entrada (indir), y los resultados, como el ajuste y la gráfica, se guardan en el directorio de salida (outdir). Si necesitas más ajustes o explicaciones, no dudes en pedírmelo.
You said:
duda rápida, si la carpeta en la que ejecuto el programa es la misma en la que están los archivos, no necesito inputdir, verdad?
ChatGPT said:
ChatGPT

Correcto, si ejecutas el programa en la misma carpeta donde están los archivos de entrada, no necesitas especificar un directorio de entrada (indir). En este caso, simplemente puedes usar los nombres de los archivos directamente en lugar de construir rutas completas. Por ejemplo:

signal_files = [
    "wzp6_ee_nuenueH_Hbb_ecm365.root",
    "wzp6_ee_numunumuH_Hbb_ecm365_vbf.root"
]

background_files = [
    "p8_ee_ZZ_ecm365.root",
    "p8_ee_WW_ecm365.root",
    "p8_ee_tt_ecm365.root",
    "wzp6_ee_numunumuH_Hbb_ecm365.root"
]

Esto simplifica el código y asume que los archivos están en el directorio de trabajo actual. Si tienes más dudas o necesitas ajustar algo en el programa, avísame. 😊
You said:
modifica el programa para que no tenga indir
ChatGPT said:
ChatGPT

El programa ha sido modificado para eliminar la dependencia de un directorio de entrada (indir). Ahora, los nombres de los archivos se especifican directamente, asumiendo que se encuentran en el mismo directorio donde se ejecuta el programa. Los resultados aún se guardarán en el directorio de salida especificado (outdir). Si necesitas más ajustes, avísame. 😊
You said:
ejecuto el programa y me sale el siguiente error: "----> ERROR: Analysis file does not contain required objects!
             Provide either RDFanalysis class, Analysis class, or build_graph function.
"
ChatGPT said:
ChatGPT

El error indica que el programa está tratando de usar algún archivo de análisis o framework del FCC que requiere estructuras específicas, como una clase RDFanalysis, Analysis, o una función build_graph, las cuales no se están proporcionando en el programa actual.

Para resolver esto, verifica lo siguiente:
1. Archivos ROOT

    ¿Contienen los histogramas con los nombres correctos? Asegúrate de que cada archivo tenga un histograma llamado jj_m. Puedes inspeccionar los archivos con ROOT:

    rootls file.root

    Esto mostrará los objetos disponibles en el archivo.

    ¿El formato es compatible? El FCC Framework puede requerir estructuras específicas de análisis, como árboles o clases de datos. Si tus archivos solo contienen histogramas y no cumplen con este formato, el programa actual debería funcionar, pero cualquier dependencia del FCC podría causar conflictos.

2. Independencia del FCC Framework

Si no necesitas interactuar con las estructuras del FCC Framework (como RDFanalysis), asegúrate de que el programa sea independiente:

    Elimina cualquier referencia o dependencia externa del framework.
    Si el problema persiste, prueba ejecutar un programa mínimo que solo cargue los histogramas y los combine para verificar que no haya problemas con ROOT.

Ejemplo de prueba básica:

import ROOT

file_name = "wzp6_ee_nuenueH_Hbb_ecm365.root"
file = ROOT.TFile.Open(file_name)
if not file or file.IsZombie():
    print(f"Error: Unable to open {file_name}")
else:
    hist = file.Get("jj_m")
    if hist:
        print(f"Histogram {hist.GetName()} loaded successfully!")
    else:
        print("Error: Histogram 'jj_m' not found.")
file.Close()

3. Adaptación al FCC Framework

Si necesitas usar herramientas específicas del FCC Framework, verifica que las dependencias estén configuradas correctamente:

    Asegúrate de cargar el entorno del FCC Framework antes de ejecutar el programa:

    source /path/to/fcc/setup.sh

    Si tu análisis requiere clases como RDFanalysis, es necesario integrarlas en el programa.

Por favor, confirma si este programa es completamente independiente o si necesitas que lo adapte al FCC Framework con las estructuras específicas. También puedes compartir más detalles del entorno en el que se está ejecutando para resolverlo con precisión.
You said:
pruebo ejecutando el programa sólo cómo python3 y el nombre del programa?
ChatGPT said:
ChatGPT

Sí, puedes ejecutar el programa directamente con:

python3 nombre_del_programa.py

Esto debería funcionar siempre y cuando:

    Instalación de ROOT: Asegúrate de que ROOT esté correctamente instalado en tu entorno y accesible desde el intérprete de Python.
    Archivos disponibles: Los archivos ROOT (wzp6_ee_nuenueH_Hbb_ecm365.root, etc.) deben estar en el mismo directorio desde el que ejecutas el programa.
    Dependencias de ROOT: Verifica que hayas configurado correctamente las variables de entorno de ROOT antes de ejecutar el script. Esto normalmente se hace con:

    source /path/to/root/bin/thisroot.sh

    Permisos de salida: La carpeta especificada en outdir debe existir o ser accesible para escribir los resultados.

Si encuentras algún problema, comparte el mensaje de error, y te ayudaré a solucionarlo. 😊
You said:
pues al ejecutarlo, me sale lo siguiente: "  File "/afs/cern.ch/user/f/fdmartin/FCCAnalyses/signal_strenght/signal_strenght.py", line 145, in <module>
    main()
  File "/afs/cern.ch/user/f/fdmartin/FCCAnalyses/signal_strenght/signal_strenght.py", line 115, in main
    signal_model = define_dscb_model(m_recoil)
  File "/afs/cern.ch/user/f/fdmartin/FCCAnalyses/signal_strenght/signal_strenght.py", line 57, in define_dscb_model
    dscb = ROOT.RooDSCBShape("dscb", "Double-Sided Crystal Ball", variable, mean, sigma, alphaL, nL, alphaR, nR)
  File "/cvmfs/sw.hsf.org/key4hep/releases/2024-03-10/x86_64-almalinux9-gcc11.3.1-opt/root/6.28.10-j6yheu/lib/root/ROOT/_facade.py", line 196, in _fallback_getattr
    raise AttributeError("Failed to get attribute {} from ROOT".format(name))
AttributeError: Failed to get attribute RooDSCBShape from ROOT
"
ChatGPT said:
ChatGPT

El error indica que la clase RooDSCBShape no está disponible en tu instalación de ROOT. Esto puede deberse a una de las siguientes razones:

    Versión de ROOT: La clase RooDSCBShape no es estándar y no está incluida en todas las versiones de ROOT. Podría estar en un paquete adicional o en un desarrollo personalizado.
    Configuración de ROOT: Puede que tu instalación de ROOT no incluya el soporte necesario para esta clase específica.

Soluciones
1. Reemplazar RooDSCBShape con una implementación alternativa

Podemos definir manualmente una función que simule el comportamiento de una Double-Sided Crystal Ball (DSCB) utilizando una combinación de funciones de ROOT, como RooGenericPdf. Aquí tienes el reemplazo:

def define_dscb_model(variable):
    """
    Define a Double-Sided Crystal Ball (DSCB) model for the signal using RooGenericPdf.
    """
    mean = ROOT.RooRealVar("mean", "Mean of DSCB", 125, 120, 130)
    sigma = ROOT.RooRealVar("sigma", "Width of DSCB", 2, 0.1, 5)
    alphaL = ROOT.RooRealVar("alphaL", "Alpha Left", 1.5, 0.1, 5)
    alphaR = ROOT.RooRealVar("alphaR", "Alpha Right", 1.5, 0.1, 5)
    nL = ROOT.RooRealVar("nL", "Power Left", 2, 0.1, 10)
    nR = ROOT.RooRealVar("nR", "Power Right", 2, 0.1, 10)

    # Define the DSCB function as a RooGenericPdf
    formula = """
    (abs(@0-@1)/@2 <= @3) * exp(-0.5*((@0-@1)/@2)^2) +
    (abs(@0-@1)/@2 > @3 && @0 < @1) * exp(-0.5*@3^2) * (1 + (@3 - abs(@0-@1)/@2)/@4)^(-@4) +
    (abs(@0-@1)/@2 > @3 && @0 > @1) * exp(-0.5*@3^2) * (1 + (@3 - abs(@0-@1)/@2)/@5)^(-@5)
    """
    dscb = ROOT.RooGenericPdf(
        "dscb", "Double-Sided Crystal Ball", formula,
        ROOT.RooArgList(variable, mean, sigma, alphaL, nL, alphaR, nR)
    )
    return dscb

# Function to define a polynomial model for the background
def define_polynomial_model(variable):
    """
    Define a first-degree polynomial model for the background.

    Args:
        variable (RooRealVar): The variable to model.

    Returns:
        RooAbsPdf: The polynomial model.
    """
    c0 = ROOT.RooRealVar("c0", "Constant Term", 0, -10, 10)
    c1 = ROOT.RooRealVar("c1", "Linear Term", 0, -10, 10)

    background = ROOT.RooPolynomial("background", "Background Model", variable, ROOT.RooArgList(c0, c1))
    return background

# Main function to perform the analysis
def main():
    # Output directory
    outdir = "/eos/user/f/fdmartin/FCC365_histograms/signal_strenght"
    os.makedirs(outdir, exist_ok=True)

    # Input files and categories
    signal_files = [
        "wzp6_ee_nuenueH_Hbb_ecm365.root",
        "wzp6_ee_numunumuH_Hbb_ecm365_vbf.root"
    ]

    background_files = [
        "p8_ee_ZZ_ecm365.root",
        "p8_ee_WW_ecm365.root",
        "p8_ee_tt_ecm365.root",
        "wzp6_ee_numunumuH_Hbb_ecm365.root"
    ]

    # Histogram names (as given)
    hist_name = "jj_m"  # Using jj_m (invariant mass of jets) as the observable

    # Load histograms
    signal_hist = load_histograms(signal_files, hist_name)
    background_hist = load_histograms(background_files, hist_name)

    if not signal_hist or not background_hist:
        print("Error: Failed to load histograms.")
        return

    # Define the observable (e.g., m_recoil)
    m_recoil = ROOT.RooRealVar("m_recoil", "Recoil Mass", 120, 140)

    # Convert histograms to RooDataHist
    signal_data = ROOT.RooDataHist("signal_data", "Signal Data", ROOT.RooArgList(m_recoil), signal_hist)
    background_data = ROOT.RooDataHist("background_data", "Background Data", ROOT.RooArgList(m_recoil), background_hist)

    # Define models
    signal_model = define_dscb_model(m_recoil)
    background_model = define_polynomial_model(m_recoil)

    # Combine signal and background models
    nsig = ROOT.RooRealVar("nsig", "Number of Signal Events", signal_hist.Integral(), 0, 1e6)
    nbkg = ROOT.RooRealVar("nbkg", "Number of Background Events", background_hist.Integral(), 0, 1e6)

    model = ROOT.RooAddPdf("model", "Signal + Background Model", ROOT.RooArgList(signal_model, background_model), ROOT.RooArgList(nsig, nbkg))

    # Perform the fit
    result = model.fitTo(signal_data, ROOT.RooFit.Save())

    # Plot the results
    canvas = ROOT.TCanvas("canvas", "Fit Results", 800, 600)
    frame = m_recoil.frame()

    signal_data.plotOn(frame)
    model.plotOn(frame)
    model.plotOn(frame, ROOT.RooFit.Components("background"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed))
    model.plotOn(frame, ROOT.RooFit.Components("dscb"), ROOT.RooFit.LineStyle(ROOT.kDotted), ROOT.RooFit.LineColor(ROOT.kBlue))

    frame.Draw()
    output_pdf = os.path.join(outdir, "fit_results.pdf")
    canvas.SaveAs(output_pdf)
    print(f"Fit results saved to {output_pdf}")

    # Print fit results
    result.Print()

if __name__ == "__main__":
    main()
