
void __thiscall
FUN__text__00409770(int param_1,short param_2,short param_3,undefined2 param_4,undefined4 param_5,
                   undefined4 param_6)

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
  if ((*(int *)(param_1 + 0x4c) == 0) &&
     (iVar2 = FUN__text__00424f80("DxSys",
                                  "E:\\CrossHermit\\GAME\\SRC\\SYSTEM\\DIRECTX\\D3dxSpFont.cpp",
                                  DAT_005ff0c4 + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*(int *)(local_8 + 0x4c) != 0) && (iVar2 = FUN__text__00409500(param_6), iVar2 == 0)) {
    *(undefined2 *)(local_8 + 0x76) = param_4;
    FUN__text__00408f10((int)param_2,(int)param_3,param_5);
  }
  local_8 = 0x409803;
  FUN__text__0056ce80();
  return;
}

