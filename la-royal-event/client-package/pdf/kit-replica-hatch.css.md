# Карточка «ищи под тем, на чём сидишь» — финальная версия (14.10)

К kit-replica.html добавлены:
- осветлённая бирюза текста: `#3d9aa6`;
- слой-сетка `.hatch` поверх всех слоёв (multiply), три направления штриховки:

```css
.hatch {
  position: absolute; inset: -4mm;
  mix-blend-mode: multiply;
  background:
    repeating-linear-gradient(48deg,  #e04438 0 0.55mm, transparent 0.55mm 2.1mm),
    repeating-linear-gradient(-41deg, #e8554a 0 0.5mm,  transparent 0.5mm  2.3mm),
    repeating-linear-gradient(7deg,   #d94a3e 0 0.45mm, transparent 0.45mm 3.1mm);
}
```

`<div class="hatch"></div>` вставляется последним элементом в `.stack` каждой карточки.
Сетка исчезает через красную линзу, бирюзовый текст остаётся.
PDF: kartochka-ishi-pod-tem.pdf (А4 альбомный, 2×А5, печатать 3 листа).
