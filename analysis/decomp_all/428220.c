
void __thiscall FUN__text__00428220(undefined2 *param_1,undefined2 param_2,short param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined2 *local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (param_3 < 1) {
    iVar2 = FUN__text__00424f80("0 < disp","E:\\CrossHermit\\GAME\\SRC\\SYSTEM\\SysListBoxCtrl.cpp",
                                DAT_005ff6c8 + 1,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *local_8 = param_2;
  local_8[1] = 0;
  local_8[2] = 0;
  local_8[3] = param_3;
  local_8 = (undefined2 *)0x42829d;
  FUN__text__0056ce80();
  return;
}

