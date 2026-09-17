
undefined1 FUN__text1__008119e1(undefined4 param_1,int *param_2,int param_3)

{
  byte bVar1;
  bool bVar2;
  undefined1 *puVar3;
  uint uVar4;
  int iVar5;
  undefined1 local_31;
  int local_24;
  uint local_1c;
  uint local_18;
  undefined1 *local_c;
  
  FUN__text1__00811873();
  FUN__text1__00811723(param_1,*param_2,0);
  puVar3 = operator_new(param_3 + 1);
  bVar2 = false;
  local_c = puVar3;
  do {
    if (bVar2) {
      *param_2 = (int)local_c - (int)puVar3;
      FUN__text1__00848490(param_1,puVar3,*param_2);
      FUN__text1__00848476(puVar3);
      FUN__text1__008118ae();
      if ((DAT_00874430 == '\0') && (local_c != puVar3 + param_3 + 1)) {
        local_31 = 1;
      }
      else {
        local_31 = 0;
      }
      return local_31;
    }
    FUN__text1__008118e1();
    local_1c = FUN__text1__00811bf4(DAT_00874444);
    if (local_1c == 0x100) {
      bVar2 = true;
    }
    *local_c = (undefined1)local_1c;
    local_c = local_c + 1;
    local_18 = local_1c;
    while (!bVar2) {
      uVar4 = FUN__text1__00811bf4(DAT_00874444);
      if (uVar4 == 0x100) {
        bVar2 = true;
        break;
      }
      if (uVar4 == 0x102) break;
      if (uVar4 == 0x101) {
        DAT_00874444 = DAT_00874444 + 1;
      }
      else {
        if (uVar4 < DAT_00874424) {
          local_24 = FUN__text1__00811ca6(0,uVar4);
        }
        else {
          *DAT_00874428 = (undefined1)local_1c;
          local_24 = FUN__text1__00811ca6(1,local_18);
        }
        bVar1 = DAT_00874428[local_24 + -1];
        local_1c = (uint)bVar1;
        for (; (local_24 != 0 && (local_c < puVar3 + param_3 + 1)); local_c = local_c + 1) {
          local_24 = local_24 + -1;
          *local_c = DAT_00874428[local_24];
        }
        iVar5 = DAT_00874448 + DAT_00874424 * 0xc;
        *(uint *)(iVar5 + 4) = local_18;
        *(byte *)(iVar5 + 8) = bVar1;
        DAT_00874424 = DAT_00874424 + 1;
        local_18 = uVar4;
      }
    }
  } while( true );
}

