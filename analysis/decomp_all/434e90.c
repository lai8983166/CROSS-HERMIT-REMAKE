
void FUN__text__00434e90(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0;
  uVar1 = FUN__text__00431d40(4);
  iVar2 = FUN__text__00469220(uVar1);
  if (iVar2 != 0) {
    local_14 = local_14 + 1;
  }
  uVar1 = FUN__text__00431d40(5);
  iVar2 = FUN__text__00469220(uVar1);
  if (iVar2 != 0) {
    local_14 = local_14 + 1;
  }
  uVar1 = FUN__text__00431d40(6);
  iVar2 = FUN__text__00469220(uVar1);
  if (iVar2 != 0) {
    local_14 = local_14 + 1;
  }
  if (local_14 != 0) {
    FUN__text__004e29a0(3,0,1);
  }
  local_10 = FUN__text__00431dd0(&DAT_005ff7fc);
  if (local_10 == 3) {
    iVar2 = FUN__text__004307b0();
    if (iVar2 == 0) {
      FUN__text__00454ab0(8);
    }
    else {
      iVar2 = FUN__text__00430ba0();
      if (iVar2 == 0) {
        FUN__text__00454ab0(5);
      }
      else {
        FUN__text__00454ab0(2);
      }
    }
  }
  else {
    local_c = FUN__text__00431d40(1);
    iVar2 = FUN__text__00469220(local_c);
    if (iVar2 == 0) {
      local_c = FUN__text__00431d40(2);
      iVar2 = FUN__text__00469220(local_c);
      if (iVar2 == 0) {
        local_c = FUN__text__00431d40(3);
        iVar2 = FUN__text__00469220(local_c);
        if (iVar2 == 0) {
          iVar2 = FUN__text__00430df0();
          if (iVar2 != 0) {
            FUN__text__00454ab0(0xe);
          }
          goto LAB__text__0043506d;
        }
        uVar1 = FUN__text__00431cc0(3);
        FUN__text__004e29a0(1,0,uVar1);
      }
      else {
        uVar1 = FUN__text__00431cc0(2);
        FUN__text__004e29a0(1,0,uVar1);
      }
    }
    else {
      uVar1 = FUN__text__00431cc0(1);
      FUN__text__004e29a0(1,0,uVar1);
    }
    FUN__text__00454ab0(0xb);
  }
LAB__text__0043506d:
  local_8 = 0x43507a;
  FUN__text__0056ce80();
  return;
}

