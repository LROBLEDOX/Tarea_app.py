import streamlit as st
import pandas as pd

#lista actividades vacia para llenar, iniciador.
if 'actividades' not in st.session_state:
    st.session_state.actividades = []

class Actividad:
    def __init__(self, nombre, tipo, presupuesto, gasto_real):
        self.nombre = nombre
        self.tipo = tipo
        self.presupuesto = presupuesto
        self.gasto_real = gasto_real

    def esta_en_presupuesto(self):
        return self.gasto_real <= self.presupuesto

    def mostrar_info(self):
        return f"Actividad: {self.nombre} | Tipo: {self.tipo} | Gasto: {self.gasto_real} / Presupuesto: {self.presupuesto}"

def calculo_retorno(actividad, tasa, meses):
    return actividad['presupuesto'] * tasa * meses

# BARRA LATERAL
st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox(
    "Seleccione un módulo:",
    ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"])

# PESTAÑA HOME
if opcion == "Home":
    st.title("Sistema de Gestión Financiera")
    st.markdown("""
    **Instrucciones:**
    * Use el menú de la izquierda para navegar.
    * En el ** MODULO 2** podrá cargar los datos que usarán los módulos 3 y 4.
    """)
    st.info("Desarrollado por: Lucia Azucena Robledo Martinez")

# --- MÓDULO: EJERCICIO 1 ---
elif opcion == "Ejercicio 1":
    st.title("Ejercicio 1")
    st.subheader("Evaluación Presupuestal")

    presupuesto = st.number_input("Ingrese su presupuesto actual:", min_value=0.00)
    gasto = st.number_input("Ingrese el monto a gastar:", min_value=0.00)

    if st.button("Evaluar Presupuesto"):
        diferencia = presupuesto - gasto
        if diferencia > 0:
            st.success("¡Gasto dentro del presupuesto!")
            st.write(f"Saldo: {diferencia}")
        else:
            st.warning("¡Presupuesto excedido!")
            st.write(f"Excede por: {abs(diferencia)}")
    
    st.divider()
    st.caption("Lucia Azucena Robledo Martinez")

# --- MÓDULO: EJERCICIO 2 ---
elif opcion == "Ejercicio 2":
    st.title("Ejercicio 2")
    st.subheader("Registro de Actividad")
    
    nombre = st.text_input("Actividad:")
    tipo = st.selectbox("Clasificación:", ["Ingreso", "Gasto Fijo", "Gasto Variable", "Inversión","Egreso"])
    presupuesto_act = st.number_input("Presupuesto asignado ($):", min_value=0.00)
    gasto_real_act = st.number_input("Gasto realizado ($):", min_value=0.00)
    saldo_real = presupuesto_act - gasto_real_act

    if st.button("Agregar Actividad"):
        if nombre:
            nueva_act = {
                "nombre": nombre,
                "tipo": tipo,
                "presupuesto": presupuesto_act,
                "gasto_real": gasto_real_act,
                "saldo_real": saldo_real
            }
            st.session_state.actividades.append(nueva_act)
            st.success(f"'{nombre}' REGISTRADA.")
        else:
            st.error("Vacío, ingrese nombre de actividad")

    if st.session_state.actividades:
        st.subheader("Lista de Actividades")
        df = pd.DataFrame(st.session_state.actividades)
        st.dataframe(df)

        st.subheader("Evaluación de Presupuesto")
        for act in st.session_state.actividades:
            if act["saldo_real"] >= 0:
                estado, icono = "Dentro del presupuesto", "✅"
            else:
                estado, icono = "Excedido", "🚨"
            st.write(f"{icono} **{act['nombre']}**: {estado} | Saldo: ${act['saldo_real']}")
    else:
        st.info("No hay actividades registradas aún.")

# --- MÓDULO: EJERCICIO 3 ---
elif opcion == "Ejercicio 3":
    st.title("Ejercicio 3")
    if st.session_state.actividades:
        st.subheader("Tasa de Retorno Mensual Esperada")

        tasa = st.slider("Indique la TRM (mensual):", min_value=0.0, max_value=1.00, value=0.05, step=0.01)
        meses = st.number_input("Cantidad de meses a proyectar:", min_value=1, value=12)

        if st.button("Calcular Proyecciones"):
            st.subheader("Resultados de la Proyección")
            proyecciones = list(map(lambda act: {
                "nombre": act['nombre'],
                "retorno": calculo_retorno(act, tasa, meses)
            }, st.session_state.actividades))

            for resultado in proyecciones:
                st.write(f"La actividad **{resultado['nombre']}** tendrá un retorno de: **${resultado['retorno']:.2f}**")
    else:
        st.warning("Primero debes registrar la actividad en el Modulo 2.")

# --- MÓDULO: EJERCICIO 4 ---
elif opcion == "Ejercicio 4":
    st.title("Ejercicio 4: POO")
    if st.session_state.actividades:
        st.subheader("Análisis de Objetos Financieros")
        
        objetos_actividad = []
        for reg in st.session_state.actividades:
            nuevo_objeto = Actividad(reg['nombre'], reg['tipo'], reg['presupuesto'], reg['gasto_real'])
            objetos_actividad.append(nuevo_objeto)

        for obj in objetos_actividad:
            st.write(obj.mostrar_info())
            if obj.esta_en_presupuesto():
                st.success(f"La actividad '{obj.nombre}' cumple.")
            else:
                st.warning(f"La actividad '{obj.nombre}' excedida.")
            st.divider()
    else:
        st.info("No hay registros previos. Regresa al Ejercicio 2.")