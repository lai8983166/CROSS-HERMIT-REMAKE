
void __fastcall FUN__text__00433bd0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 0x2e6f8) < 0x1a5e0) {
    local_c = FUN__text__00431f50(&DAT_005ff788);
    if (local_c == 3) {
      FUN__text__00454ab0(0xf);
    }
    else {
      iVar1 = FUN__text__00430df0();
      if (iVar1 != 0) {
        FUN__text__00454ab0(0xe);
      }
    }
  }
  else {
    local_c = FUN__text__00431dd0(&DAT_005ff788);
    local_10 = FUN__text__00431dd0(&DAT_005ff790);
    local_14 = FUN__text__00431dd0(&DAT_005ff794);
    if (((local_c == 3) && (local_10 == 1)) && (local_14 == 2)) {
      iVar1 = FUN__text__00430ba0();
      if (iVar1 == 0) {
        FUN__text__00454ab0(5);
      }
      else {
        FUN__text__00454ab0(2);
      }
    }
    else if (local_c == 3) {
      FUN__text__00454ab0(8);
    }
    else {
      FUN__text__00454ab0(0xb);
    }
  }
  local_8 = 0x433cf7;
  FUN__text__0056ce80();
  return;
}

