
void __fastcall FUN__text__00453e10(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)(param_1 + 0xc0) = 0;
  *(undefined2 *)(param_1 + 0xde) = 200;
  local_8 = param_1;
  FUN__text__00407870(0x5a,0);
  FUN__text__004079c0(0,0);
  *(undefined2 *)(local_8 + 0xc0) = 0;
  *(undefined2 *)(local_8 + 0xde) = 200;
  FUN__text__00407870(0x5a,1);
  FUN__text__004079c0(0x18c,600);
  *(undefined2 *)(local_8 + 0xc0) = 0;
  *(undefined2 *)(local_8 + 0xde) = 200;
  FUN__text__00407870(0x5a,2);
  FUN__text__004079c0(0x31a,600);
  FUN__text__00467c20(199);
  FUN__text__00458e30();
  FUN__text__00456b20();
  local_8 = 0x453f0b;
  FUN__text__0056ce80();
  return;
}

