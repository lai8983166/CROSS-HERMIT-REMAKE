
void __fastcall FUN__text__004cab80(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [12];
  undefined4 uStack_18;
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  FUN__text__0056de40(param_1 + 0x18,0x110,10,FUN__text__004cab40);
  uStack_18 = 0x4cabc2;
  FUN__text__0056ce80();
  return;
}

