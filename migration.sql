CREATE TABLE public.train (
  semana INTEGER,
  agencia_id INTEGER,
  canal_id INTEGER,
  ruta_sak INTEGER,
  cliente_id INTEGER,
  producto_id INTEGER,
  venta_uni_hoy INTEGER,
  venta_hoy NUMERIC(10,2),
  dev_uni_proxima INTEGER,
  dev_proxima NUMERIC(10,2),
  demanda_uni_equil INTEGER
);