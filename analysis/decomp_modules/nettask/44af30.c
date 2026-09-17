
void __fastcall FUN__text__0044af30(int param_1)

{
  char cVar1;
  undefined1 uVar2;
  undefined2 uVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_6c [16];
  int local_2c;
  int local_28;
  int local_24;
  uint local_20;
  int local_1c;
  int local_18;
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar5 = local_6c;
  for (iVar4 = 0x1a; iVar4 != 0; iVar4 = iVar4 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_24 = param_1 + 0x1a54;
  local_8 = param_1;
  iVar4 = FUN__text__00441b90();
  if (iVar4 == 0) {
    local_10 = 0;
    local_20 = *(uint *)(DAT_007a49fc + 0x199c) & 1;
    local_14 = 0x18;
    local_c = FUN__text__0044c710(&DAT_00606498,0x18);
    if (local_c != -1) {
      if (local_20 != 0) {
        local_2c = local_c;
        switch(local_c) {
        case 0:
          FUN__text__00428720();
          FUN__text__004db2b0(5);
          break;
        case 1:
          FUN__text__00428810();
          FUN__text__004db2b0(5);
          break;
        case 2:
          FUN__text__00428850();
          FUN__text__004db2b0(5);
          break;
        case 3:
          FUN__text__00428760();
          FUN__text__004db2b0(5);
          break;
        default:
          iVar4 = FUN__text__004283b0();
          local_18 = local_c + -4 + iVar4 * 4;
          if (local_18 < 0x1e) {
            FUN__text__0044aee0(local_18);
            FUN__text__004db2b0(5);
            FUN__text__00442f40();
          }
        }
      }
      if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) != 0) {
        FUN__text__0044b170(local_c);
      }
    }
    local_1c = FUN__text__004128f0(0x1d,0);
    iVar4 = FUN__text__004128f0(0x9d,0);
    local_1c = local_1c + iVar4;
    if ((local_1c != 0) && (iVar4 = FUN__text__004128f0(0x1e,1), iVar4 != 0)) {
      FUN__text__0044ae70();
      FUN__text__00442f40();
    }
    cVar1 = FUN__text__0041ad60();
    local_28 = (int)cVar1;
    uVar2 = FUN__text__0044ac50();
    *(undefined1 *)(local_8 + local_28 + 0x1a95) = uVar2;
    uVar3 = FUN__text__0044acd0();
    *(undefined2 *)(local_8 + 0x1a9a + local_28 * 2) = uVar3;
  }
  local_8 = 0x44b14d;
  FUN__text__0056ce80();
  return;
}

