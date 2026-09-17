
void __fastcall FUN__text__0053f973(uint param_1)

{
  uint uVar1;
  uint *puVar2;
  uint uVar3;
  uint *puVar4;
  uint local_8;
  
  if (*(int *)(param_1 + 0xb0) != 0) {
    puVar2 = *(uint **)(param_1 + 0xb8);
    uVar3 = *(int *)(param_1 + 0xc4) - (int)puVar2;
    local_8 = param_1;
    FUN__text__00548e1c((uVar3 + 3 & 0x3fffc) * 0x4000 + 0x10000 & 0x7fff0000 | 0xfffe);
    FUN__text__00548e1c(0x54584554);
    *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 8;
    if (3 < uVar3) {
      local_8 = uVar3 >> 2;
      do {
        FUN__text__00548e1c(*puVar2);
        *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 4;
        puVar2 = puVar2 + 1;
        uVar3 = uVar3 - 4;
        local_8 = local_8 - 1;
      } while (local_8 != 0);
      local_8 = 0;
    }
    if (uVar3 != 0) {
      local_8 = 0;
      puVar4 = &local_8;
      for (uVar1 = uVar3 >> 2; uVar1 != 0; uVar1 = uVar1 - 1) {
        *puVar4 = *puVar2;
        puVar2 = puVar2 + 1;
        puVar4 = puVar4 + 1;
      }
      for (uVar1 = uVar3 & 3; uVar1 != 0; uVar1 = uVar1 - 1) {
        *(char *)puVar4 = (char)*puVar2;
        puVar2 = (uint *)((int)puVar2 + 1);
        puVar4 = (uint *)((int)puVar4 + 1);
      }
      FUN__text__00548e1c(local_8);
      *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 4;
    }
    if (uVar3 == 4) {
      FUN__text__00548e1c(0);
      *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 4;
    }
  }
  return;
}

