select u.nombre,
    u.correo,
    pr.nombre,
    mr.nombre,
    emr.cantidad,
    emr.condiciones_entrega,
    from entrega_material_reciclado as emr
    INNER JOIN material_reciclable as mr on emr.id_material = mr.id_material
    INNER JOIN entregas as e on emr.id_entrega = e.id_entrega
    INNER JOIN puntos_reciclaje as pr on e.punto_entrega = pr.id_punto
    INNER JOIN usuarios as u on e.id_usuario_e = u.id_usuario
where pr.id_recicladora = 1;