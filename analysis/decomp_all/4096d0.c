
void __thiscall
FUN__text__004096d0(int param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4,
                   undefined4 param_5)

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
                                  DAT_005ff0c0 + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((*(int *)(local_8 + 0x4c) != 0) && (iVar2 = FUN__text__00409440(), iVar2 != 0)) {
    FUN__text__00409770(param_2,CONCAT22((short)((uint)*(undefined4 *)(local_8 + 0x80) >> 0x10),
                                         param_3),param_4,param_5,*(undefined4 *)(local_8 + 0x80));
  }
  local_8 = 0x409763;
  FUN__text__0056ce80();
  return;
}

