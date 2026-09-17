
undefined4 FUN_005709d0(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  undefined1 local_38 [8];
  int local_30;
  int local_2c;
  int local_24;
  
  FUN_005702d0(local_38);
  if (((local_24 == 0) && (local_30 == 0)) && (((DAT_007619c0 & 0x10) == 0 || (local_2c == 0)))) {
    uVar3 = 0;
  }
  else {
    iVar2 = FUN_00573780(0,0,0,0,&DAT_00592a18,"Detected memory leaks!\n");
    if (iVar2 == 1) {
      pcVar1 = (code *)swi(3);
      uVar3 = (*pcVar1)();
      return uVar3;
    }
    FUN_005705b0(0);
    uVar3 = 1;
  }
  return uVar3;
}

