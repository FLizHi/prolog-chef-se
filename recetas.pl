% 1. HECHOS (Ingredientes base de cada receta)
% Receta 1: Quesadillas de quesillo con epazote
ingrediente_receta(quesadillas_quesillo, tortillas_de_harina).
ingrediente_receta(quesadillas_quesillo, quesillo_deshebrado).
ingrediente_receta(quesadillas_quesillo, epazote_fresco).

% Receta 2: Minipizza de sartén 
ingrediente_receta(minipizza_sarten, tortillas_de_harina).
ingrediente_receta(minipizza_sarten, quesillo_deshebrado).
ingrediente_receta(minipizza_sarten, salsa_de_tomate).
ingrediente_receta(minipizza_sarten, pepperoni).

% Receta 3: Burritos norteños de pollo y quesillo con vegetales salteados (pimiento morrón, cebolla y chile serrano) 
ingrediente_receta(burritos_nortenos, tortillas_de_harina).
ingrediente_receta(burritos_nortenos, quesillo_deshebrado).
ingrediente_receta(burritos_nortenos, pollo_deshebrado).
ingrediente_receta(burritos_nortenos, pimiento_morron_salteado).
ingrediente_receta(burritos_nortenos, cebolla_salteada).
ingrediente_receta(burritos_nortenos, chile_serrano).

% Receta 4: Tostadas de tinga de pollo 
ingrediente_receta(tinga_de_pollo, pollo_deshebrado).
ingrediente_receta(tinga_de_pollo, tostadas).
ingrediente_receta(tinga_de_pollo, dos_jitomates).
ingrediente_receta(tinga_de_pollo, cebolla_en_rodajas).
ingrediente_receta(tinga_de_pollo, un_chile_chipotle).

% Receta 5: Tostadas de pollo con crema y lechuga 
ingrediente_receta(tostadas_de_pollo, pollo_deshebrado).
ingrediente_receta(tostadas_de_pollo, tostadas).
ingrediente_receta(tostadas_de_pollo, crema).
ingrediente_receta(tostadas_de_pollo, lechuga).


% HECHOS ALTERNATIVOS O SUSTITUTOS
ingrediente_alternativo(pollo, pollo_deshebrado).
ingrediente_alternativo(pollo, pollo_asado).
ingrediente_alternativo(pollo, pollo_rostizado).

ingrediente_alternativo(tortillas_de_harina, tortillas_de_maiz).

ingrediente_alternativo(quesillo_deshebrado, queso_gouda).
ingrediente_alternativo(quesillo_deshebrado, queso_asadero).
ingrediente_alternativo(quesillo_deshebrado, queso_panela).

ingrediente_alternativo(dos_jitomates, caja_de_caldillo_de_tomate).
ingrediente_alternativo(cebolla_en_rodajas, caja_de_caldillo_de_tomate).
ingrediente_alternativo(un_chile_chipotle, caja_de_caldillo_de_tomate).

% HECHOS DE CATEGORÍA / tipo de comida
tipo_receta(quesadillas_quesillo, desayuno).
tipo_receta(minipizza_sarten, comida).
tipo_receta(burritos_nortenos, comida).
tipo_receta(tinga_de_pollo, comida).
tipo_receta(tostadas_de_pollo, cena).


% 2. REGLAS 

% Regla 1. Verificar si una receta es de un tipo determinado
es_del_momento(Receta, Momento) :-
tipo_receta(Receta, Momento).

% Regla 2. Regla de Ingrediente alternativo o sustituto
recomendar_receta(Receta, IngredienteUsuario) :-
ingrediente_receta(Receta, IngredienteRequerido),
    (IngredienteRequerido == IngredienteUsuario ; ingrediente_alternativo(IngredienteRequerido, IngredienteUsuario)).

% Regla 3. Recomendar por categoría (tipo de comida)
recomendar_por_categoria(Receta, TipoDeseado, IngredienteUsuario) :-
recomendar_receta(Receta, TipoDeseado),
tipo_receta(Receta, IngredienteUsuario).

% Regla 4. Recomendar desayuno
recomendar_desayuno(Receta, IngredienteUsuario) :-
    tipo_receta(Receta, desayuno),
    recomendar_receta(Receta, IngredienteUsuario).

% Regla 5. Recomendar comida
recomendar_comida(Receta, IngredienteUsuario) :-
    tipo_receta(Receta, comida),
    recomendar_receta(Receta, IngredienteUsuario).

% Regla 6. Recomendar cena
recomendar_cena(Receta, IngredienteUsuario) :-
    tipo_receta(Receta, cena),
    recomendar_receta(Receta, IngredienteUsuario).

% Regla 7. Reglas de Seguridad Alimentaria y Exclusión
receta_sin_carne(Receta) :-
tipo_receta(Receta, _), % Asegura que sea una receta válida
\+ ingrediente_receta(Receta, pollo_deshebrado),
\+ ingrediente_receta(Receta, pepperoni).

% Regla 8. Receta sin lácteos
receta_sin_lacteos(Receta) :-
    tipo_receta(Receta, _),
    \+ ingrediente_receta(Receta, quesillo_deshebrado),
    \+ ingrediente_receta(Receta, crema).

% Regla 9. Receta vegetariana
recomendar_vegetariano(Receta, IngredienteUsuario) :-
    receta_sin_carne(Receta),
    recomendar_receta(Receta, IngredienteUsuario).

% Regla 10. Verificar si una receta contine picante
contiene_picante(Receta, IngredientePicante) :-
    ingrediente_receta(Receta, IngredientePicante),
    (IngredientePicante == un_chile_chipotle ; IngredientePicante == chile_serrano).

