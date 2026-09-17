
void FUN__text__0040ed20(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined2 param_4
                        ,undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_44c [16];
  int local_40c;
  undefined1 local_408 [1024];
  undefined1 *local_8;
  
  puVar3 = local_44c;
  for (iVar2 = 0x112; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = &stack0x00000020;
  local_40c = FUN__text__0056dbb0(local_408,param_7,local_8);
  local_8 = (undefined1 *)0x0;
  if (0x3ff < local_40c) {
    iVar2 = FUN__text__00424f80("ret<1024","E:\\CrossHermit\\GAME\\src\\system\\directx\\DxDraw.cpp"
                                ,DAT_005ff360 + 9,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  FUN__text__0040ec50(param_2,param_3,CONCAT22((short)((uint)local_408 >> 0x10),param_4),param_5,
                      param_6,local_408);
  local_8 = (undefined1 *)0x40edcc;
  FUN__text__0056ce80();
  return;
}

