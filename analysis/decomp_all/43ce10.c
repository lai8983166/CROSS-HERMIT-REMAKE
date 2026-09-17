
void __fastcall FUN__text__0043ce10(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((*(int *)(param_1 + 0x2659c) == 0) &&
     (iVar2 = FUN__text__00424f80("MapCw!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ffa0c + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(int *)(local_8 + 0x2659c) != 0) {
    FUN__text__0043cf10();
    iVar2 = FUN__text__0043cfe0(local_8 + 0x98);
    if (((iVar2 == 0) && (iVar2 = FUN__text__0043cfe0(local_8 + 0x9c), iVar2 == 0)) &&
       (iVar2 = FUN__text__0043cfe0(local_8 + 0xa0), iVar2 == 0)) {
      *(undefined4 *)(local_8 + 0xa4) = *(undefined4 *)(local_8 + 0x98);
      *(undefined4 *)(local_8 + 0xa8) = *(undefined4 *)(local_8 + 0x9c);
    }
    else {
      FUN__text__0043cf10();
    }
  }
  local_8 = 0x43cf0c;
  FUN__text__0056ce80();
  return;
}

