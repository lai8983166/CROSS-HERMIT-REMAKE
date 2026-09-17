
void __thiscall FUN__text__00410270(undefined4 *param_1,int param_2,undefined2 param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  code *local_14;
  int local_10;
  undefined4 local_c;
  undefined4 *local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = param_2;
  local_14 = *(code **)(param_2 + 8);
  local_8 = param_1;
  if (local_14 == (code *)0x0) {
    iVar2 = FUN__text__00424f80("CallFunc!=0",
                                "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxDraw.cpp",
                                DAT_005ff364 + 6,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (*local_14)(CONCAT22((short)((uint)local_8[1] >> 0x10),param_3),*local_8,local_8[1],
              *(undefined4 *)(local_10 + 0xc));
  local_c = FUN__text__0056ce80();
  local_8 = (undefined4 *)0x410301;
  FUN__text__0056ce80();
  return;
}

