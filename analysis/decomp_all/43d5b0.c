
void __thiscall FUN__text__0043d5b0(int param_1,undefined2 param_2,undefined2 param_3)

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
  if (0x27 < *(int *)(param_1 + 0x263c8)) {
    iVar2 = FUN__text__00424f80("SmcWork.cnt < 40",
                                "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",DAT_005ffa18 + 1,
                                0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined2 *)(local_8 + 0x263cc + *(int *)(local_8 + 0x263c8) * 4) = param_2;
  *(undefined2 *)(local_8 + 0x263ce + *(int *)(local_8 + 0x263c8) * 4) = param_3;
  *(int *)(local_8 + 0x263c8) = *(int *)(local_8 + 0x263c8) + 1;
  local_8 = 0x43d64f;
  FUN__text__0056ce80();
  return;
}

