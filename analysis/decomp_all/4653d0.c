
void FUN__text__004653d0(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058fe64;
  local_10 = ExceptionList;
  puVar4 = local_60;
  for (iVar3 = 0x14; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004649c0();
  local_8 = 0;
  FUN__text__004646e0();
  local_8._0_1_ = 1;
  FUN__text__0043a060();
  local_8._0_1_ = 2;
  FUN__text__0044e280();
  local_8._0_1_ = 3;
  FUN__text__004378d0();
  local_8._0_1_ = 4;
  FUN__text__0040ba20();
  local_8._0_1_ = 5;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0xdb86c),0x88,0x14,FUN__text__00465ac0,FUN__text__00465b00);
  local_8._0_1_ = 6;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0xde460),0x28,2,FUN__text__00427530,FUN__text__004275b0);
  local_8._0_1_ = 7;
  FUN__text__004075e0();
  local_8._0_1_ = 8;
  FUN__text__004075e0();
  local_8._0_1_ = 9;
  FUN__text__004075e0();
  local_8._0_1_ = 10;
  FUN__text__004075e0();
  local_8._0_1_ = 0xb;
  FUN__text__004075e0();
  local_8._0_1_ = 0xc;
  FUN__text__004075e0();
  local_8._0_1_ = 0xd;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0xde7b0),0x80,3,FUN__text__004075e0,FUN__text__00407710);
  local_8._0_1_ = 0xe;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0xde930),0x80,0x40,FUN__text__004075e0,FUN__text__00407710);
  local_8._0_1_ = 0xf;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0xe0930),0x80,0x200,FUN__text__004075e0,FUN__text__00407710);
  local_8._0_1_ = 0x10;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0xf0930),0x80,0x200,FUN__text__004075e0,FUN__text__00407710);
  local_8._0_1_ = 0x11;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0x100930),0x80,0x100,FUN__text__004075e0,FUN__text__00407710);
  local_8._0_1_ = 0x12;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0x108930),0x80,4,FUN__text__004075e0,FUN__text__00407710);
  local_8._0_1_ = 0x13;
  _eh_vector_constructor_iterator_
            ((void *)(local_14 + 0x116098),0x2c,10,FUN__text__00465b40,FUN__text__00465b80);
  local_8 = CONCAT31(local_8._1_3_,0x14);
  _memset((void *)(local_14 + 0x2a6e8),0,8);
  FUN__text__00466ab0();
  _memset((void *)(local_14 + 0x80aec),0,0x50140);
  _memset((void *)(local_14 + 0xdb818),0,0x50);
  _memset((void *)(local_14 + 0x30998),0,0x14);
  _memset((void *)(local_14 + 0x309ac),0,0x50140);
  _memset((void *)(local_14 + 0xd0c2c),0,44000);
  _memset((void *)(local_14 + 0xdb86c),0,0xaa0);
  _memset((void *)(local_14 + 0x2c6f0),0,0x2000);
  _memset((void *)(local_14 + 0x2c6f0),0,0x2000);
  _memset((void *)(local_14 + 0x2c6f0),0,0x2000);
  _memset((void *)(local_14 + 0xdc310),0,1000);
  _memset((void *)(local_14 + 0x108b60),0,1000);
  _memset((void *)(local_14 + 0xdc8ec),0,0x139c);
  *(undefined4 *)(local_14 + 0xdc30c) = 0;
  *(undefined4 *)(local_14 + 0x108b50) = 0;
  FUN__text__00492e90();
  FUN__text__00494cf0();
  FUN__text__00494d20();
  FUN__text__004077c0(DAT_007a49fc);
  *(undefined4 *)(local_14 + 0x108f74) = 0;
  *(undefined2 *)(local_14 + 0x108b32) = 0;
  *(undefined2 *)(local_14 + 0x10f9c2) = 0xffff;
  *(undefined2 *)(local_14 + 0x10f9c0) = 0xffff;
  *(undefined1 *)(local_14 + 0x10f9c4) = 0;
  *(undefined1 *)(local_14 + 0x2ef44) = 0;
  for (local_18 = 0; local_18 != 0x10; local_18 = local_18 + 1) {
    *(undefined2 *)(local_14 + 0x2ef14 + local_18 * 2) = 0;
  }
  for (local_18 = 0; local_18 != 0x10; local_18 = local_18 + 1) {
    *(undefined1 *)(local_14 + local_18 + 0x2ef34) = 0;
  }
  _memset((void *)(local_14 + 0x2e714),0,0x800);
  FUN__text__00467db0();
  if (local_14 == 0) {
    local_1c = 0;
  }
  else {
    local_1c = local_14 + 0x3d68;
  }
  FUN__text__00437a30(local_1c);
  if (local_14 == 0) {
    local_20 = 0;
  }
  else {
    local_20 = local_14 + 0x3d68;
  }
  FUN__text__0044e810(local_20);
  FUN__text__00427650(0xfa);
  (*API_GDI32_DLL_CreateFontA)(0xc,0,0,0,400,0,0,0,1,5,0,0,0,&DAT_00592c9c);
  uVar2 = FUN__text__0056ce80();
  *(undefined4 *)(local_14 + 0xdb80c) = uVar2;
  if (*(int *)(local_14 + 0xdb80c) == 0) {
    iVar3 = FUN__text__00424f80("tFont!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618b10 + 0x2f,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  (*API_GDI32_DLL_CreateFontA)(0xc,0,0,0,400,0,0,0,1,5,0,0,0,&DAT_00592c9c);
  uVar2 = FUN__text__0056ce80();
  *(undefined4 *)(local_14 + 0xdb810) = uVar2;
  if (*(int *)(local_14 + 0xdb810) == 0) {
    iVar3 = FUN__text__00424f80("tFontMsp!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618b10 + 0x33,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined4 *)(local_14 + 0x2e6f0) = 0;
  _memset((void *)(local_14 + 0x108b3e),0,0x10);
  FUN__text__0049cc10();
  FUN__text__00493dc0();
  *(undefined4 *)(local_14 + 0x117c38) = 0;
  *(undefined1 *)(local_14 + 0x108b3b) = 0xff;
  *(undefined1 *)(local_14 + 0x108b3c) = 0;
  FUN__text__004077c0(DAT_007a49fc);
  FUN__text__004077c0(DAT_007a49fc);
  FUN__text__004077c0(DAT_007a49fc);
  FUN__text__004077c0(DAT_007a49fc);
  FUN__text__004077c0(DAT_007a49fc);
  FUN__text__004077c0(DAT_007a49fc);
  FUN__text__00496390(0);
  *(undefined4 *)(local_14 + 0x117c40) = 0;
  *(undefined1 *)(local_14 + 0x2ef45) = 0;
  FUN__text__004935f0();
  local_8 = 0xffffffff;
  ExceptionList = local_10;
  FUN__text__0056ce80();
  return;
}

