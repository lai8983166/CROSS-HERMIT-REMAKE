
void FUN__text__00412810(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_1 < 0) &&
     (iVar2 = FUN__text__00424f80("0<=lx","E:\\CrossHermit\\GAME\\src\\system\\directx\\DxInput.cpp"
                                  ,DAT_005ff48c + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if ((param_2 < 0) &&
     (iVar2 = FUN__text__00424f80("0<=ly","E:\\CrossHermit\\GAME\\src\\system\\directx\\DxInput.cpp"
                                  ,DAT_005ff48c + 2,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_8 = 0x4128b3;
  FUN__text__0056ce80();
  return;
}

