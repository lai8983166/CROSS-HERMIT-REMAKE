
void __fastcall FUN__text__004727f0(int param_1)

{
  undefined1 uVar1;
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
  uVar1 = FUN__text__0040a100(param_1 + 0x109388);
  *(undefined1 *)(local_8 + 0x109344) = uVar1;
  *(short *)(local_8 + 0x10934a) = *(short *)(local_8 + 0x10934a) + 1;
  local_8 = 0x472852;
  FUN__text__0056ce80();
  return;
}

