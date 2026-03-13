# F35 Notes

- O worker deve usar politica `skip e seguir` para runs incompatíveis de outro principal.
- Runs incompatíveis permanecem pendentes e destravadas para um runtime compativel futuro.
- Runs legadas continuam compativeis para evitar regressao do backlog criado antes do binding autenticado do runtime.
- O recorte nao muda a CLI publica nem adiciona eventos novos.
