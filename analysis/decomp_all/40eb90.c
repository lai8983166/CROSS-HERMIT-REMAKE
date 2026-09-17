
void FUN__text__0040eb90(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1;
  if ((1 < *(byte *)(param_1 + 0x10)) &&
     (iVar2 = FUN__text__00424f80("ft->off < 2",
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxDraw.cpp",
                                  DAT_005ff35c + 2,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_14 = (int)*(short *)(local_c + 10);
  local_18 = (int)*(short *)(local_c + 8);
  local_10 = FUN__text__00402780((float)local_18,(float)local_14,*(undefined4 *)(local_c + 0xc),
                                 local_c + 0x11,0);
  local_8 = 0x40ec49;
  FUN__text__0056ce80();
  return;
}

